from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('', views.index, name='index'),
    
]