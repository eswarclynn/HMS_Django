from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name= 'django_auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate-email/', ActivationEmailResendView.as_view(), name='send_activate_email'),
    path('activate/<uidb64>/<token>/', account_activate, name='account_activate'),
    path('activation-email-sent/', ActivationEmailSentView.as_view(), name='account_activation_sent'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password-sent/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]