from django import forms
from powerline.models import PowerLine, DispatchCompanies, ThirdPartyDispatchers

class PowerLineForm(forms.Form):
    power_line = forms.ChoiceField(choices=(), label='Выберите наименованеи ВЛ')
    dispatchers = forms.ModelChoiceField(queryset=ThirdPartyDispatchers.objects.none(), label='Выберите ФИО диспетчера, отдавшего команду')
    