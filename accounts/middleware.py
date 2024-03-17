from django.utils import timezone
from django.db.models import F
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

User = get_user_model()

class FailedLoginAttemptsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # If the user is attempting to log in and the request method is POST
        if request.method == 'POST' and 'email' in request.POST and 'password' in request.POST:
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                if user.is_locked:
                    return HttpResponseForbidden("Your account is locked. Please contact support.")
                else:
                    # Check password, if incorrect, increment failed login attempts
                    if not user.check_password(request.POST['password']):
                        user.failed_login_attempts = F('failed_login_attempts') + 1
                        user.save()
                        # Lock the account after a certain number of failed attempts
                        max_failed_attempts = 5
                        actual_failed_attempts = User.objects.get(email=email).failed_login_attempts
                        if actual_failed_attempts >= max_failed_attempts:
                            user.failed_login_attempts = 0  # Reset failed attempts
                            user.is_locked = True
                            user.save()
                        return HttpResponseForbidden("Incorrect password. Please try again.")
                    else:
                        # Reset failed login attempts upon successful authentication
                        user.failed_login_attempts = 0
                        user.save()
            except User.DoesNotExist:
                pass
        return response
