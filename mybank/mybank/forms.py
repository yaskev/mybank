from django import forms
from django.contrib.auth.models import User

from .models import Client, Admin, Account


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
    currency = forms.ChoiceField(choices=(('RUR', 'RUR'), ('USD', 'USD'),
                                          ('EUR', 'EUR')))
    balance = forms.DecimalField(min_value=0)


class TransferForm(forms.Form):
    send_account = forms.ModelChoiceField(queryset=Account.objects.all())
    receiver = forms.ModelChoiceField(queryset=Client.objects.all())


class AdvancedTransferForm(TransferForm):
    receiver_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(decimal_places=2)
    comment = forms.CharField(max_length=256)

    def clean(self):
        data = super().clean()
        amount = data.get('amount')
        sender_balance = data.get('send_account').balance
        receiver = data.get('receiver')
        receiver_account = data.get('receiver_account')

        if amount > sender_balance:
            raise forms.ValidationError('Not enough money')

        if receiver_account not in receiver.accounts.all():
            raise forms.ValidationError('Invalid receiver account')
