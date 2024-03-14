from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone
from el_journals.settings import (FILE_UPLOAD_MAX_MEMORY_SIZE,
                                  REVERSE_EDITING_PERIOD)
from multiupload.fields import MultiFileField
from powerline.models import AdmittingStaff, PowerLine, ThirdPartyDispatchers
from substation.models import Substation

from .models import AutofillDispModel, MainPageOPJournal, СommentOPJ

CustomUser = get_user_model()


class MainPageOPJournalForm(forms.ModelForm):
    existing_entry = forms.ModelChoiceField(
        queryset=MainPageOPJournal.objects.filter(entry_is_valid=True,),
        required=False,
        label='Выберите существующую запись'
    )
    work_entry = forms.ModelChoiceField(
        queryset=MainPageOPJournal.objects.filter(entry_is_valid=True,),
        required=False,
        label='Выберите существующую запись'
    )
    important_event_checkbox = forms.BooleanField(
        required=False,
        label='Вывод из работы/отключение')
    permission_to_work_checkbox = forms.BooleanField(
        required=False,
        label='Допуск к выполнению работ')
    pub_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now().strftime('%Y-%m-%dT%H:%M')
    )
    planned_completion_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now().strftime('%Y-%m-%dT%H:%M')
    )
    text = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'autocomplete-text',
        'wrap': 'soft'}))
    substation = forms.ModelChoiceField(
        queryset=Substation.objects.all(),
        widget=forms.HiddenInput())
    file = MultiFileField(min_num=1,
                          max_num=5,
                          max_file_size=FILE_UPLOAD_MAX_MEMORY_SIZE,
                          required=False)

    def __init__(self, *args, **kwargs):
        substation_slug = kwargs.pop('substation_slug', None)
        super(MainPageOPJournalForm, self).__init__(*args, **kwargs)
        now1 = timezone.localtime(timezone.now())
        now1 = now1.replace(minute=0)  # обнуляем минуты
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()).strftime('%Y-%m-%dT%H:%M')
        self.fields['planned_completion_date'].initial = now1.strftime(
            '%Y-%m-%dT%H:%M')

        if substation_slug:
            substation = Substation.objects.get(slug=substation_slug)
            existing_entry_queryset = MainPageOPJournal.objects.filter(
                entry_is_valid=True,
                withdrawal_for_repair=True,
                closing_entry=None,
                substation=substation
            )
            self.fields['existing_entry'].queryset = existing_entry_queryset
            work_entry_queryset = MainPageOPJournal.objects.filter(
                entry_is_valid=True,
                permission_to_work=True,
                closing_entry=None,
                substation=substation
            )
            self.fields['work_entry'].queryset = work_entry_queryset

            self.fields['text'].widget = forms.Textarea(attrs={
                'autocomplete': 'off',
                'data-autocomplete-url': reverse(
                    'substation_autocomplete',
                    args=[substation_slug]) if substation_slug else '',
                'wrap': 'soft',

            })

    def get_initial(self):
        initial = super().get_initial()
        if self.instance and self.instance.important_event_checkbox:
            initial['important_event_checkbox'] = True
        else:
            initial['important_event_checkbox'] = False
        return initial

    def clean_pub_date(self):
        pub_date = self.cleaned_data['pub_date']
        current_time = timezone.now()
        time_difference = current_time - pub_date
        if time_difference.total_seconds() < 0:
            raise forms.ValidationError('Введенная дата '
                                        'не может быть '
                                        'больше текущей!')
        if time_difference.total_seconds() > REVERSE_EDITING_PERIOD * 3600:
            if (REVERSE_EDITING_PERIOD % 10 == 1
                    and REVERSE_EDITING_PERIOD != 11):
                hour = 'час'
            elif (2 <= REVERSE_EDITING_PERIOD % 10 <= 4
                    and REVERSE_EDITING_PERIOD < 10
                    or REVERSE_EDITING_PERIOD > 20):
                hour = 'часа'
            else:
                hour = 'часов'
            raise forms.ValidationError('Введённая дата не '
                                        'может быть меньше текущей '
                                        'более, чем на '
                                        f'{REVERSE_EDITING_PERIOD} {hour}!')
        return pub_date

    def clean_planned_completion_date(self):
        important_event_checkbox = self.cleaned_data.get(
            'important_event_checkbox')
        planned_completion_date = self.cleaned_data.get(
            'planned_completion_date')

        if important_event_checkbox:
            if (planned_completion_date
                    and planned_completion_date) <= timezone.now():
                raise forms.ValidationError('Планируемая дата '
                                            'ввода в работу оборудования '
                                            'должна быть в будущем.')
        return planned_completion_date

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            for f in file:
                if f.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                    raise forms.ValidationError('Превышен максимальный '
                                                'размер файла',
                                                code='file_size_exceeded')
        return file

    def save(self, commit=True):
        instance = super().save(commit=False)
        withdrawal_for_repair = self.cleaned_data.get(
            'withdrawal_for_repair')
        planned_completion_date = self.cleaned_data.get(
            'planned_completion_date')

        if withdrawal_for_repair and not planned_completion_date:
            instance.planned_completion_date = datetime(2200, 1, 1, 0, 0, 0)

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = MainPageOPJournal
        fields = ['text',
                  'pub_date',
                  'substation',
                  'special_regime_introduced',
                  'emergency_event',
                  'short_circuit',
                  'file',
                  'important_event_checkbox',
                  'permission_to_work_checkbox',
                  'existing_entry',
                  'work_entry',
                  'planned_completion_date',]


class OPJournalForm(forms.ModelForm):
    planned_completion_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now().strftime('%Y-%m-%dT%H:%M'),
        required=False  # делаем поле необязательным
    )

    def clean(self):
        cleaned_data = super().clean()
        planned_completion_date = cleaned_data.get('planned_completion_date')
        if not planned_completion_date:
            cleaned_data['planned_completion_date'] = (
                self.instance.planned_completion_date)
        return cleaned_data

    def clean_planned_completion_date(self):
        planned_completion_date = self.cleaned_data.get(
            'planned_completion_date')
        initial_planned_completion_date = (
            self.instance.planned_completion_date
            if self.instance.pk
            else None)
        withdrawal_for_repair = (
            self.instance.withdrawal_for_repair
            if self.instance.pk
            else False)
        closing_entry = (
            self.instance.closing_entry
            if self.instance.pk
            else None)

        if withdrawal_for_repair and not closing_entry:
            if (planned_completion_date
                    and initial_planned_completion_date
                    and (planned_completion_date
                         < initial_planned_completion_date)):
                raise forms.ValidationError('Дата продления не может быть '
                                            'меньше, указанной ранее, при '
                                            'выводе оборудования из работы!')

        return planned_completion_date

    class Meta:
        model = MainPageOPJournal
        fields = ['entry_is_valid', 'planned_completion_date']

        widgets = {
            'entry_is_valid': forms.CheckboxInput(attrs={
                'class': 'form-check-input'})}


class CommentOPJForm(forms.ModelForm):
    class Meta:
        model = СommentOPJ
        fields = ['text']


class AutofillDispForm(forms.ModelForm):
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now().strftime('%Y-%m-%dT%H:%M')
    )
    name = forms.ModelChoiceField(
        queryset=PowerLine.objects.all(),
        to_field_name='name')
    dispatcher = forms.ModelChoiceField(
        queryset=ThirdPartyDispatchers.objects.all(),
        to_field_name='disp_name')
    admitting = forms.ModelChoiceField(
        queryset=AdmittingStaff.objects.all(),
        to_field_name='name')
    ending = forms.ModelChoiceField(
        queryset=Substation.objects.all(),
        to_field_name='name')

    def __init__(self, *args, **kwargs):
        autofill_disp_queryset = kwargs.pop('autofill_disp_queryset', None)
        super(AutofillDispForm, self).__init__(*args, **kwargs)
        now1 = timezone.localtime(timezone.now())
        now1 = now1.replace(minute=0)
        self.fields['end_time'].initial = now1.strftime('%Y-%m-%dT%H:%M')
        if autofill_disp_queryset is not None:
            self.fields['name'].queryset = autofill_disp_queryset

    class Meta:
        model = AutofillDispModel
        fields = ['name',
                  'dispatcher',
                  'end_time',
                  'emergency_entry',
                  'cus_dispatcher',
                  'admitting',
                  'ending']
        widgets = {
            'hand_over_text': forms.Textarea(attrs={'readonly': 'readonly'})
        }
