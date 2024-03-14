from django import forms

from .models import Substation


class SubstationForm(forms.ModelForm):
    class Meta:
        model = Substation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubstationForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields[
                'dispatcher_for'
            ].queryset = Substation.objects.exclude(id=instance.id)
