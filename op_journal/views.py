from io import BytesIO
import pytz
import os
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib import pdfencrypt

from docx import Document
from django.template import Context
from docxtpl import DocxTemplate
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Pt
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Cm, Inches
import io
import docx
import codecs
import pytz


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.db.models import Q
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from datetime import datetime, timedelta
from django.utils import timezone

from op_journal.models import MainPageOPJournal, AutocompleteOption
from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE, STATICFILES_DIRS, STATIC_URL, MEDIA_URL, MEDIA_ROOT
from .forms import MainPageOPJournalForm, OPJournalForm, CommentOPJForm
from substation.models import Substation

import PyPDF2
from PyPDF2 import PdfFileWriter


@login_required(login_url='/login/')
def op_journal_detail(request, pk):
    op_journal_entry = get_object_or_404(MainPageOPJournal, pk=pk)
    return render(request, 'op_journal/op_journal_detail.html', {'op_journal_entry': op_journal_entry})

def op_journal_edit(request, pk):
    op_journal_entry = get_object_or_404(MainPageOPJournal, pk=pk)
    if request.user == op_journal_entry.user:
        if op_journal_entry.entry_is_valid:
            if request.method == "POST":
                form = OPJournalForm(request.POST, instance=op_journal_entry)
                if form.is_valid():
                    op_journal_entry = form.save(commit=False)
                    if not op_journal_entry.entry_is_valid:
                        op_journal_entry.special_regime_introduced = False
                        op_journal_entry.emergency_event = False
                        op_journal_entry.short_circuit = False
                    op_journal_entry.save()
                    return HttpResponseRedirect(reverse('sub_op_journal', kwargs={'substation_slug': op_journal_entry.substation.slug}))
            else:
                form = OPJournalForm(instance=op_journal_entry)
            return render(request, 'op_journal/op_journal_edit.html', {'op_journal_entry': op_journal_entry, 'form': form})
        else:
            return redirect('op_journal_detail', pk=pk)
    else:
        return redirect('op_journal_detail', pk=pk)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class OpJournalView(ListView, FormView):
    template_name = 'op_journal/index.html'
    context_object_name = 'model_op_journal_data'
    paginate_by = NUMBER_ENTRIES_OP_LOG_PAGE
    extra_context = {'title': 'Инструкция по ведению электронного оперативного журнала'}
    form_class = MainPageOPJournalForm
    comment_form_class = CommentOPJForm
    
    
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if 'reset' in request.POST:
            return self.reset_search()
        return super().post(request, *args, **kwargs)
    
    def reset_search(self):
        substation_slug = self.kwargs.get('substation_slug')
        return HttpResponseRedirect(reverse('sub_op_journal', args=[substation_slug]))

    def get_queryset(self):
        substation_slug = self.kwargs.get('substation_slug')
        query = self.request.GET.get('query')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        queryset = MainPageOPJournal.objects.filter(substation__slug=substation_slug).order_by('-pub_date', '-id')
        if query:
            queryset = queryset.filter(text__icontains=query)
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            queryset = queryset.filter(Q(pub_date__date__gte=start_date, pub_date__date__lte=end_date))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substation_slug = self.kwargs.get('substation_slug', None)
        if substation_slug:
            substation = Substation.objects.get(slug=substation_slug)
            context['substation'] = substation
            if self.object_list.exists():
                substation_name = self.object_list[0].substation.name
                context['head'] = f"Оперативный журнал {substation_name}"
                context['title'] = f"Оперативный журнал {substation_name}"
                context['substation_slug'] = substation_slug
            else:
                context['head'] = "Оперативный журнал"
                context['title'] = "Оперативный журнал"
            form = MainPageOPJournalForm(initial={'substation': substation}, substation_slug=substation_slug, request=self.request)
        else:
            form = MainPageOPJournalForm(request=self.request)
        context['form'] = form
        comment_form = self.comment_form_class()
        context['comment_form'] = comment_form
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        substation_slug = self.kwargs.get('substation_slug', None)
        if substation_slug:
            substation = Substation.objects.get(slug=substation_slug)
            context['substation'] = substation
        context['form'] = form
        context['text_value'] = form.cleaned_data['text']
        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        op_journal = form.save()
        return HttpResponseRedirect(reverse('sub_op_journal', args=[form.instance.substation.slug]))

def autocomplete_view(request, substation_slug):
    substation = get_object_or_404(Substation, slug=substation_slug)
    query = request.GET.get('term', '')
    options = AutocompleteOption.objects.filter(substation=substation, text__icontains=query)
    results = [option.text for option in options]
    return JsonResponse(results, safe=False)

def add_comment(request, post_id):
    post = get_object_or_404(MainPageOPJournal, pk=post_id)

    if request.method == 'POST':
        comment_form = CommentOPJForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.save()
            post.comment = comment
            post.save()
    return HttpResponseRedirect(reverse('sub_op_journal', args=[post.substation.slug]))


def export_records(request, substation_slug):
    start_date = timezone.make_aware(datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d'))
    end_date = timezone.make_aware(datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d'))
    end_date += timedelta(days=1)
    queryset = MainPageOPJournal.objects.filter(pub_date__range=[start_date, end_date], substation__slug=substation_slug)
    # Загрузка шаблона Word
    template = docx.Document('templates/op_journal/template.docx')
    substation_name = Substation.objects.get(slug=substation_slug).name
    for paragraph in template.paragraphs:
        if 'PLACEHOLDER_FOR_SUBSTATION_NAME' in paragraph.text:
            for run in paragraph.runs:
                if 'PLACEHOLDER_FOR_SUBSTATION_NAME' in run.text:
                    run.text = run.text.replace('PLACEHOLDER_FOR_SUBSTATION_NAME', substation_name)
            break
    # Поиск таблицы в шаблоне
    table = template.tables[0]
    # Получение локальной временной зоны сервера
    local_timezone = pytz.timezone('Europe/Moscow')  # Замените 'Europe/Moscow' на соответствующую временную зону
    # Заполнение таблицы данными из запроса
    for record in queryset:
        row = table.add_row().cells
        # Преобразование времени в локальную временную зону
        local_time = record.pub_date.astimezone(local_timezone)
        row[0].text = local_time.strftime('%d.%m.%Y\n%H:%M')
        row[1].text = f'{record.text}\n{record.user.position} {record.user}'
        row[2].text = f'{record.comment.text}\n{record.comment.user.position} {record.comment.user}' if record.comment else ""
    # Сохранение документа во временный буфер
    output = io.BytesIO()
    template.save(output)
    # Настройка HTTP-ответа
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=exported_records.docx'
    output.seek(0)
    response.write(output.getvalue())
    output.close()
    return response