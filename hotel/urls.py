'''from django.urls import path
from .views import LoginView, HomeView, CustomLogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
]
'''