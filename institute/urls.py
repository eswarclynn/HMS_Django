from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery',views.gallery, name='gallery'),
    path('block-gallery/',views.hostels,name='hostels'),
    path('contact/',views.contact,name='contact'),
    path('developer-team/',views.developers, name='developers'),

]