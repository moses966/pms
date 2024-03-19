from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser


User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    def form_invalid(self, form):
        # Fetch email from form data
        email = form.cleaned_data.get('username')
        
        try:
            user = User.objects.get(email=email)
            max_failed_attempts = 3
            remaining_attempts = max_failed_attempts - user.failed_login_attempts

            if user.is_locked:
                pass
                # Add a warning message for locked account
                messages.error(self.request, _("Your account is locked. Please contact support for assistance."))
                return super().form_invalid(form)
            else:
                # Add a warning message for incorrect password entry
                messages.error(self.request, _(f"Incorrect password. {remaining_attempts} attempts remaining."))
                return super().form_invalid(form)
        except User.DoesNotExist:
            # This block handles the case when the user doesn't exist
            messages.warning(self.request, _("User with this email does not exist. Please try again."))
            return super().form_invalid(form)
        except Exception as e:
            # Handle other exceptions and display error message
            messages.error(self.request, str(e))
            return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            if user.is_locked:
                # Add error message for locked account
                return self.form_invalid(form)
            else:
                login(self.request, user)
                return super().form_valid(form)
        else:
            form.add_error(None, "Incorrect email or password")
            return self.form_invalid(form)

    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class LockedAccountView(TemplateView):
    template_name = 'accounts/locked_account.html' 
