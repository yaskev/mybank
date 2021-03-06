import requests

from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


from .forms import SignUpForm, CreateAccountForm,\
                    TransferForm, AdvancedTransferForm
from .models import Client, Account, Transaction

RATES_URL = 'https://api.exchangerate-api.com/v4/latest/'


class SignUpView(TemplateView):
    form_class = SignUpForm
    initial = {}
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Client.objects.create_user(username=data['email'],
                                       email=data['email'],
                                       password=data['password1'],
                                       first_name=data['name'],
                                       last_name=data['surname'])
            return HttpResponseRedirect('/login/')

        return render(request, self.template_name, {'form': form})


class MainView(TemplateView):
    template_name = 'main.html'
    success = False

    @method_decorator(login_required)
    def get(self, request, account, *args, **kwargs):
        return render(request, self.template_name,
                      {'chosen_account': Account.objects.get(id=account),
                       'trans': Transaction.objects.filter(
                           Q(sender=account) | Q(receiver=account))[:10],
                       'successful_transfer': self.success
                       })


class AccountManager(TemplateView):
    template_name = 'accounts.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'accounts': Client.objects.get
                       (id=request.user.id).accounts.all()})


class AccountDeletion(TemplateView):
    template_name = 'accounts.html'

    @method_decorator(login_required)
    def get(self, request, account, *args, **kwargs):
        Client.objects.get(id=request.user.id).delete_account(account)
        return HttpResponseRedirect('/accounts')


class CreateAccountView(TemplateView):
    template_name = 'creation.html'
    form_class = CreateAccountForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'accounts': Client.objects.get
                       (id=request.user.id).accounts.all()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = Client.objects.get(id=request.user.id)
            Account.objects.create(currency=data['currency'],
                                   balance=data['balance'],
                                   owner=user)
            return HttpResponseRedirect('/accounts')

        return render(request, self.template_name, {'form': form})


class TransferView(TemplateView):
    template_name = 'transfer.html'
    form_class = TransferForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'client_accounts': Client.objects.get
                       (id=request.user.id).accounts.all(),
                       'rec_list': Client.objects.all()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            from_curr = data['send_account'].currency
            if from_curr == 'RUR':
                from_curr = 'RUB'
            prices = requests.get(RATES_URL + from_curr).json()['rates']

            return render(request, self.template_name,
                          {'source_account': data['send_account'],
                           'receiver': data['receiver'],
                           'advanced': True,
                           'rec_accounts': data['receiver'].accounts.all(),
                           'USD': round(prices['USD'], 4),
                           'EUR': round(prices['EUR'], 4),
                           'RUR': round(prices['RUB'], 4)
                           })

        return render(request, self.template_name, {'form': form})


class AdvancedTransferView(TemplateView):
    template_name = 'transfer.html'
    form_class = AdvancedTransferForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        from_curr = Account.objects.get(id=int(form.data['send_account'])).currency
        if from_curr == 'RUR':
            from_curr = 'RUB'
        prices = requests.get(RATES_URL + from_curr).json()['rates']

        if form.is_valid():
            data = form.cleaned_data
            destination_currency = data['receiver_account'].currency
            if destination_currency == 'RUR':
                destination_currency = 'RUB'
            transaction_rate = round(prices[destination_currency], 4)
            data['send_account'].owner.transfer(data['send_account'],
                                                data['receiver_account'],
                                                data['amount'],
                                                data['comment'],
                                                transaction_rate)

            return HttpResponseRedirect('/feed/success/' +
                                        str(data['send_account'].id))

        data = form.data
        source_account = Account.objects.get(id=int(data['send_account']))
        receiver = Client.objects.get(id=int(data['receiver']))
        rec_counts = receiver.accounts.all()

        return render(request, self.template_name,
                      {'form': form,
                       'source_account': source_account,
                       'receiver': receiver,
                       'advanced': True,
                       'rec_accounts': rec_counts,
                       'toUSD': prices['USD'],
                       'toEUR': prices['EUR'],
                       'toRUR': prices['RUB'],
                       })
