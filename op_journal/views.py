from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from op_journal.models import MainPageOPJournal, AutocompleteOption
from el_journals.settings import NUMBER_ENTRIES_OP_LOG_PAGE
from .forms import MainPageOPJournalForm, OPJournalForm
from substation.models import Substation

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
    
    
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        substation_slug = self.kwargs.get('substation_slug')
        queryset = MainPageOPJournal.objects.filter(substation__slug=substation_slug).order_by('-pub_date')
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
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        substation_slug = self.kwargs.get('substation_slug', None)
        if substation_slug:
            substation = Substation.objects.get(slug=substation_slug)
            context['substation'] = substation
        context['form'] = form
        context['text_value'] = form.cleaned_data['text']  # Добавляем значение поля Text в контекст
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        op_journal = form.save()
        return HttpResponseRedirect(reverse('sub_op_journal', args=[form.instance.substation.slug]))

def autocomplete_view(request, substation_slug):
    substation = get_object_or_404(Substation, slug=substation_slug)
    form = MainPageOPJournalForm(substation_slug=substation_slug)
    query = request.GET.get('term', '')
    options = AutocompleteOption.objects.filter(substation=substation, text__icontains=query)
    results = [option.text for option in options]
    return JsonResponse(results, safe=False)