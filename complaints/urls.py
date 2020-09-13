from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name= 'complaints'

urlpatterns = [
    path('register-complaint/', login_required(views.registerComplaint), name='registerComplaint'),
]