"""
URL configuration for TelegramBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# urls.py
from django.urls import path
from .views import SignupView, SigninView, SendMessageView

urlpatterns = [
    path('auth/signup', SignupView.as_view(), name='signup'),
    path('auth/signin', SigninView.as_view(), name='signin'),
    path('telegram/send_message', SendMessageView.as_view(), name='send_message'),
]