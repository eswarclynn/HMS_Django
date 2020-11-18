from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import User
from .forms import SignUpForm, LoginForm, ActivationEmailForm
from institute.models import Student, Official
from workers.models import Worker
from django.contrib.auth import login, get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

User = get_user_model()

# Create your views here.

class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name='django_auth/login.html'
    form_class = LoginForm

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
        return reverse('django_auth:account_activation_sent')

    def form_valid(self, form):
        form.instance.email_confirmed = False

        response = super().form_valid(form)
        
        # After save, send confirmation email
        user = form.instance
        user.send_activation_email(self.request)
        
        # After save assign to entity!
        is_student = form.cleaned_data.get('is_student')
        is_official = form.cleaned_data.get('is_official')
        is_worker = form.cleaned_data.get('is_worker')
        email = form.cleaned_data.get('email')

        if is_student:
            Student.objects.filter(account_email = email).update(user = user)
        elif is_official:
            Official.objects.filter(account_email = email).update(user = user)
        elif is_worker:
            Worker.objects.filter(account_email = email).update(user = user)
        return response
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_title'] = 'Sign Up'
        return context

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        messages.success(request, 'Account email verified!')
        login(request, user)
        return redirect(user.home_url())
    else:
        return render(request, 'django_auth/account_activation_invalid.html', {'form_title': 'Account Activation Failed'})

class ActivationEmailResendView(FormView):
    template_name = 'django_auth/password_change.html'
    form_class = ActivationEmailForm
    success_url = reverse_lazy('django_auth:account_activation_sent')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = User.objects.filter(email = email, is_active = True, email_confirmed = False)
        for user in users:
            user.send_activation_email(self.request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Send Account Activation Email'
        return context

class ActivationEmailSentView(TemplateView):
    template_name = 'django_auth/account_activation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Account Activation Email sent'
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
