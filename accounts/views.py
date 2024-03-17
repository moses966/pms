from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from .forms import CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect


User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    #authentication_form = CustomAuthenticationForm
    authentication_form = CustomAuthenticationForm

    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') # Redirect to login page after logout
