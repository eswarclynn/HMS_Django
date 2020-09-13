from django.urls import path
from . import views

app_name= 'workers'

urlpatterns = [
    path('staff-home/', views.staff_home, name='staff_home'),
    path('medical/', views.medical_issue, name='medical_issue')

]