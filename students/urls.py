from django.urls import path

from . import views

app_name= 'students'

urlpatterns = [
    path('student-home/', views.student_home, name='student_home'),
    path('outing-application', views.outing_app, name='outing_app'),
    path('attendance_history', views.attendance_history, name='attendance_history'),
    path('outing_history', views.outing_history, name='outing_history'),

]