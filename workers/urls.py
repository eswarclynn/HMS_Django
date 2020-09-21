from django.urls import path
from . import views

app_name= 'workers'

urlpatterns = [
    path('home/', views.home, name='home'),
]