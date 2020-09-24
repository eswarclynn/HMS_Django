from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives

class UserManager(BaseUserManager):
    def create_user(self, email, type_flag, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        if type_flag == 'student':
            user.is_student = True
        elif type_flag == 'official':
            user.is_official = True
        elif type_flag == 'worker':
            user.is_worker = True
        else:
            raise ValueError('User type should be one of the following:\n student, official, worker')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        
        user = self.create_user(email=email, password=password, type_flag='official')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=250,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    email_confirmed = models.BooleanField(default=True)

    #Add eMail here when both username(id) and eMail required
    # REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'

    def home_url(self):
        if self.is_student:
            return reverse('students:home')
        elif self.is_official:
            return reverse('officials:home')
        elif self.is_worker:
            return reverse('workers:home')

    def send_activation_email(self, request, from_email=None, **kwargs):
        current_site = get_current_site(request)
        subject = 'Activate your Hostel Management System Account.'
        email_context = {
            'user': self,
            'protocol': request.scheme,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': account_activation_token.make_token(self),
        }
        email_template = 'django_auth/account_activation_email_text.html'
        html_email_template = 'django_auth/account_activation_email_html.html'
        
        self.email_user(subject, email_context, email_template, html_email_template)


    def email_user(self, subject, context, email_template, html_email_template, from_email=None, **kwargs):
        body = render_to_string(email_template, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [self.email])
        html_email = render_to_string(html_email_template, context)
        email_message.attach_alternative(html_email, 'text/html')
        email_message.send()
