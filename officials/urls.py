from django.urls import path
from django.views.generic import FormView
from . import views
from .forms import StudentForm

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

    path('register-student/', views.StudentRegisterView.as_view(), name='register_student'),
    path('edit-student/<int:pk>', views.StudentUpdateView.as_view(), name='edit_student'),
    path('register-official/', views.OfficialRegisterView.as_view(), name='register_official'),
    path('edit-official/<int:pk>', views.OfficialUpdateView.as_view(), name='edit_official'),
    path('register-staff/', views.WorkerRegisterView.as_view(), name='register_worker'),
    path('edit-staff/<int:pk>', views.WorkerUpdateView.as_view(), name='edit_worker'),


    path('water-cans/', views.watercan, name='watercan'),
    path('student_list/', views.student_list, name='student_list'),
    path('emp_list/',views.emp_list,name="emp_list"),
    path('empdelete/',views.empdelete,name="empdelete"),
    path('workers_list/',views.workers_list,name="workers_list"),
    path('workerdelete/',views.workerdelete,name="workerdelete"),
]