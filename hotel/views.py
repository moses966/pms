'''from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views import View
from .forms import LoginForm

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'hotel/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the home page or dashboard after successful login
                return redirect('home')
            else:
                # Handle invalid credentials
                error_message = "Invalid email or password."
                return render(request, 'hotel/login.html', {'form': form, 'error_message': error_message})
        else:
            # Form is invalid
            return render(request, 'hotel/login.html', {'form': form})

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class CustomLogoutView(LogoutView):
    # Redirect to home page after logging out
    next_page = reverse_lazy('home')
'''