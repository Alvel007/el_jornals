from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import CustomUser, Substation


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class StaffListView(ListView):
    template_name = 'staff/index.html'
    context_object_name = 'model_user_data'
    paginate_by = 20
    extra_context = {'title': 'Персонал'}

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            return CustomUser.objects.filter(is_public=True).order_by('-id')
        substation = get_object_or_404(Substation, slug=slug)
        operational_staff = substation.operational_staff.filter(is_public=True)
        administrative_staff = substation.administrative_staff.filter(
            is_public=True)
        return (operational_staff | administrative_staff).distinct().order_by(
            'administrative_staff', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            substation = get_object_or_404(Substation, slug=slug)
            context['substation'] = substation
            context['operational_staff'] = substation.operational_staff.filter(
                id__in=self.get_queryset().values('id'))
            context['administrative_staff'] = (substation.
                                               administrative_staff.
                                               filter(
                                                   id__in=(self.
                                                           get_queryset().
                                                           values('id'))))
            context['head'] = f'Информация о персонале {substation.name}'
            context['slug'] = True
        else:
            context['head'] = 'Информация о персонале'
        return context
