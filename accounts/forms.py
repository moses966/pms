from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the password field
        self.fields['password'].strip = False
        self.fields['password'].widget = forms.PasswordInput()

        # Rename the username field to email
        self.fields['username'].label = _('Email')
        self.fields['username'].widget = forms.EmailInput(attrs={'autofocus': True})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if email and password:
            # Perform any additional validation here
            pass

        return cleaned_data