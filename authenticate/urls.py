from django.urls import path

from . import views

app_name= 'authenticate'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.forgot, name='forgot')
]