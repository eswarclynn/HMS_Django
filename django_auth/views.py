from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import User
from .forms import SignUpForm
from institute.models import Student, Official
from workers.models import Worker

# Create your views here.

class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name='django_auth/login.html'

    def get_success_url(self):
        return self.request.user.home_url()

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_title'] = 'Log In'
        return context

class SignUpView(CreateView):
    template_name = 'django_auth/signup.html'
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('django_auth:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        is_student = form.cleaned_data.get('is_student')
        is_official = form.cleaned_data.get('is_official')
        is_worker = form.cleaned_data.get('is_worker')
        entity_id = form.cleaned_data.get('entity_id')
        if is_student:
            Student.objects.filter(regd_no = entity_id).update(user = form.instance)
        elif is_official:
            Official.objects.filter(emp_id = entity_id).update(user = form.instance)
        elif is_worker:
            Worker.objects.filter(staff_id = entity_id).update(user = form.instance)

        return response
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_title'] = 'Sign Up'
        return context

class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'django_auth/password_change.html'

    def get_success_url(self):
        return self.request.user.home_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Change Password'
        return context


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'django_auth/password_change.html'
    subject_template_name = 'django_auth/password_reset_subject.txt'
    email_template_name = 'django_auth/password_reset_email_text.html'
    html_email_template_name = 'django_auth/password_reset_email_html.html'
    success_url = reverse_lazy('django_auth:password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Reset Password'
        return context

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'django_auth/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Reset Password eMail Sent'
        return context

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'django_auth/password_reset_confirm.html'
    success_url = reverse_lazy('django_auth:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Reset New Password'
        return context

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'django_auth/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Password Reset Complete'
        return context
