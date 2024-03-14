from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control',
            'id': 'newUser',
            'type': 'text',
            'value': '',
            'name': 'newPassword2'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'newPassword',
                'type': 'text',
                'value': '',
                'name': 'user_pass',
                'style': '-webkit-text-security: disc;',
                'onfocus': 'this.removeAttribute("readonly");',
                'onblur': 'this.setAttribute("readonly", "readonly");'
            }
        )
    )
