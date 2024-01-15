from django import forms
from django.forms import FileField
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import MainPageOPJournal, СommentOPJ
from django.shortcuts import get_object_or_404, render
from multiupload.fields import MultiFileField


from el_journals.settings import REVERSE_EDITING_PERIOD, FILE_UPLOAD_MAX_MEMORY_SIZE
from django.shortcuts import redirect, reverse
from substation.models import Substation

CustomUser = get_user_model()

class MainPageOPJournalForm(forms.ModelForm): 
    existing_entry = forms.ModelChoiceField(
        queryset=MainPageOPJournal.objects.filter(entry_is_valid=True, important_event_date_start__isnull=False, important_event_date_over__isnull=True),
        required=False,
        label='Выберите существующую запись'
    )
    important_event_checkbox = forms.BooleanField(required=False, label='Вывод в ремонт/допуск бригады') 
    pub_date = forms.DateTimeField( 
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), 
        input_formats=['%Y-%m-%dT%H:%M'], 
        initial=timezone.now().strftime('%Y-%m-%dT%H:%M') 
    ) 
    text = forms.CharField(widget=forms.Textarea(attrs={'id': 'autocomplete-text'})) 
    substation = forms.ModelChoiceField(queryset=Substation.objects.all(), widget=forms.HiddenInput()) 
    file = MultiFileField(min_num=1, max_num=5, max_file_size=FILE_UPLOAD_MAX_MEMORY_SIZE, required=False) 

    def __init__(self, *args, **kwargs):
        substation_slug = kwargs.pop('substation_slug', None)
        super(MainPageOPJournalForm, self).__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M')
        if substation_slug:
            substation = Substation.objects.get(slug=substation_slug)
            self.fields['existing_entry'].queryset = MainPageOPJournal.objects.filter(
                entry_is_valid=True,
                important_event_date_start__isnull=False,
                important_event_date_over__isnull=True,
                substation=substation
            )
        self.fields['text'].widget = forms.TextInput(attrs={
            'autocomplete': 'off',
            'data-autocomplete-url': reverse('substation_autocomplete', args=[substation_slug])
        })

    def clean_pub_date(self):
        pub_date = self.cleaned_data['pub_date']
        current_time = timezone.now()
        time_difference = current_time - pub_date
        if time_difference.total_seconds() < 0:
            raise forms.ValidationError('Введенная дата не может быть больше текущей!')
        if time_difference.total_seconds() > REVERSE_EDITING_PERIOD * 3600:
            print('привет')
            if REVERSE_EDITING_PERIOD % 10 == 1 and REVERSE_EDITING_PERIOD != 11:
                hour = 'час'
            elif 2 <= REVERSE_EDITING_PERIOD % 10 <= 4 and (REVERSE_EDITING_PERIOD < 10 or REVERSE_EDITING_PERIOD > 20):
                hour = 'часа'
            else:
                hour = 'часов'
            raise forms.ValidationError(f'Введённая дата не может быть меньше текущей более, чем на {REVERSE_EDITING_PERIOD} {hour}!')
        print('хуйня')
        return pub_date
    
    def save(self, commit=True):
        instance = super(MainPageOPJournalForm, self).save(commit=False)
        if commit:
            instance.save()
            existing_entry = self.cleaned_data['existing_entry']
            if existing_entry:
                existing_entry.important_event_date_over = instance.pub_date
                existing_entry.save()
        return instance

    class Meta: 
        model = MainPageOPJournal 
        fields = ['text', 'pub_date', 'substation', 'special_regime_introduced', 'emergency_event', 'short_circuit', 'file', 'important_event_checkbox', 'existing_entry']

class OPJournalForm(forms.ModelForm):
    class Meta:
        model = MainPageOPJournal
        fields = ['entry_is_valid']

        widgets = {
            'entry_is_valid': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        
class CommentOPJForm(forms.ModelForm):
    class Meta:
        model = СommentOPJ
        fields = ['text']