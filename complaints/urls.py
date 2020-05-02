from django.urls import path

from . import views

app_name= 'complaints'

urlpatterns = [
    path('register-complaint/', views.registerComplaint, name='registerComplaint'),

]