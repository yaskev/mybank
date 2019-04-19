from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import Client


class LoginView(TemplateView):
    template_name = 'login.html'


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
            return HttpResponse('User created successfully')

        return render(request, self.template_name, {'form': form})
