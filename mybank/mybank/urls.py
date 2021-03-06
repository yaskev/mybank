"""mybank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from .views import SignUpView,\
                    MainView, \
                    AccountManager, \
                    AccountDeletion, \
                    CreateAccountView, \
                    TransferView, \
                    AdvancedTransferView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('signup/', SignUpView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('feed/<int:account>', MainView.as_view()),
    path('feed/success/<int:account>', MainView.as_view(success=True)),
    path('feed/', TemplateView.as_view(template_name='feed.html')),
    path('accounts/delete/<int:account>', AccountDeletion.as_view()),
    path('accounts/', AccountManager.as_view()),
    path('newaccount/', CreateAccountView.as_view()),

    path('transfer/next/', AdvancedTransferView.as_view()),
    path('transfer/', TransferView.as_view()),
]
