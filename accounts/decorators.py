from functools import wraps
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

def check_account_lock(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_locked:
            messages.error(request, "Your account is locked. Please contact support.")
            return redirect(reverse('login'))
        return func(request, *args, **kwargs)
    return wrapper
