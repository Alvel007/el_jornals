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
            self.fields['dispatcher_for'].queryset = Substation.objects.exclude(id=instance.id)
        
        """if not self.initial.get('dispatch_point', False):
            self.fields['dispatcher_for'].widget.attrs['disabled'] = True
            self.fields['dispatcher_for'].required = False"""


"""    def save(self, commit=True):
        instance = super(SubstationForm, self).save(commit=False)
        if commit:
            instance.save()
            #instance.dispatcher_for.clear()
            #dispatcher_for = self.cleaned_data.get('dispatcher_for', None)
            #if dispatcher_for is not None:
            #    instance.dispatcher_for.set(dispatcher_for)
        return instance"""