from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.urls import reverse
from .models import User
from .forms import SignUpForm

# Create your views here.

class LoginView(auth_views.LoginView):
    template_name='django_auth/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_student:
            return reverse('students:student_home')
        elif user.is_official:
            return reverse('officials:official_home')
        elif user.is_official:
            return reverse('workers:staff_home')

class SignUpView(CreateView):
    template_name = 'django_auth/signup.html'
    form_class = SignUpForm

    def get_success_url(self):
        user = self.object
        if user.is_student:
            return reverse('students:student_home')
        elif user.is_official:
            return reverse('officials:official_home')
        elif user.is_official:
            return reverse('workers:staff_home')

class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'django_auth/password_change.html'


    

