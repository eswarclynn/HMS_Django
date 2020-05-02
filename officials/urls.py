from django.urls import path

from . import views

app_name= 'officials'

urlpatterns = [
    path('warden-home/', views.official_home, name='official_home'),
    path('warden-profile/', views.profile, name='profile'),
    path('attendance/', views.takeAttendance, name='attendance'),
    path('grant-outing/', views.grantOuting, name='grantOuting'),
    path('chief-profile/', views.chiefsProfile, name='chiefsProfile'),
    # path('board-profile')
]