from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings

from . import views

app_name= 'officials'

urlpatterns = [
    path('warden-home/', views.official_home, name='official_home'),
    path('warden-profile/', views.profile, name='profile'),
    path('attendance/', views.takeAttendance, name='attendance'),
    path('attendance-staff/', views.attendance_workers, name='attendance_workers'),
    path('attendance-log/', views.attendance_log, name='attendance_log'),
    path('grant-outing/', views.grantOuting, name='grantOuting'),
    path('chief-profile/', views.chiefsProfile, name='chiefsProfile'),
    path('block-search/', views.blockSearch, name='blockSearch'),
    path('search/',views.search, name='search'),
    path('register-student/', views.register, name='register'),
    path('register-employee/', views.registeremp, name='registeremp'),
    path('water-cans/', views.watercan, name='watercan'),
    path('student_list/', views.student_list, name='student_list'),
    path('student-edit/', views.studentdelete, name='studentdelete'),
    path('emp_list/',views.emp_list,name="emp_list"),
    path('empdelete/',views.empdelete,name="empdelete"),
    path('registerworker/',views.registerworker,name="registerworker"),
    path('workers_list/',views.workers_list,name="workers_list"),
    path('workerdelete/',views.workerdelete,name="workerdelete"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)