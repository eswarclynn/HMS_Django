from django.urls import path

from . import views

app_name= 'institute'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery',views.gallery, name='gallery'),
    path('search-result/',views.search,name='search'),
    path('block-gallery/',views.hostels,name='hostels'),
    path('contact/',views.contact,name='contact'),

]