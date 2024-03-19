from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class FailedLoginAttemptsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ Code to be executed for each request before
            the view (and later middleware) are called.
        """
        # If the user is attempting to log in and the request method is POST
        if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
            email = request.POST['username']
            try:
                user = User.objects.get(email=email)
                if user.is_locked:
                    # Redirect the user to a locked account message page
                    return HttpResponseRedirect(reverse('locked_account'))
                else:
                    # Check password, if incorrect, increment failed login attempts
                    if not user.check_password(request.POST['password']):
                        user.failed_login_attempts += 1
                        user.save()
                        # Lock the account after a certain number of failed attempts
                        max_failed_attempts = 3
                        if user.failed_login_attempts >= max_failed_attempts:
                            user.failed_login_attempts = 0
                            user.is_locked = True
                            user.save()
                            # Redirect the user to a locked account message page
                            return HttpResponseRedirect(reverse('locked_account'))
                    else:
                        # Reset failed login attempts upon successful authentication
                        user.failed_login_attempts = 0
                        user.save()
            except User.DoesNotExist:
                pass
        response = self.get_response(request)
        """Code to be executed for each request/response after
           the view is called.
        """

        return response
