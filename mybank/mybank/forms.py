from django import forms
from django.contrib.auth.models import User

from .models import Client, Admin


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        pass1 = data.get('password1')
        pass2 = data.get('password2')
        if pass1 != pass2:
            raise forms.ValidationError('Passwords must match')

        if User.objects.filter(email=data.get('email')).exists():
            raise forms.ValidationError('Not unique email')


class CreateAccountForm(forms.Form):
    currency = forms.ChoiceField(choices=(('RUR', 'RUR'), ('USD', 'USD'), ('EUR', 'EUR')))
    balance = forms.DecimalField(min_value=0)
