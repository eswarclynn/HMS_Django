from django.urls import path
from django.views.generic import FormView, DeleteView
from django.conf.urls.static import static 
from django.conf import settings

from . import views
from .forms import StudentForm

app_name= 'officials'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance-staff/', views.attendance_workers, name='attendance_workers'),
    path('attendance-log/', views.attendance_log, name='attendance_log'),
    path('generate-attendance-sheet/', views.generate_attendance_sheet, name='generate_attendance_sheet'),
    path('grant-outing/', views.grant_outing, name='grant_outing'),
    path('outing/<int:pk>', views.outing_detail, name='outing_detail'),
    path('block-layout/', views.blockSearch, name='blockSearch'),
    # path('search/',views.search, name='search'),

    path('student-list/', views.StudentListView.as_view(), name='student_list'),
    path('register-student/', views.StudentRegisterView.as_view(), name='register_student'),
    path('edit-student/<int:pk>', views.StudentUpdateView.as_view(), name='edit_student'),
    path('delete-student/<int:pk>', views.StudentDeleteView.as_view(), name='delete_student'),

    path('official-list/',views.OfficialListView.as_view(),name="emp_list"),
    path('register-official/', views.OfficialRegisterView.as_view(), name='register_official'),
    path('edit-official/<int:pk>', views.OfficialUpdateView.as_view(), name='edit_official'),
    path('delete-official/<int:pk>', views.OfficialDeleteView.as_view(), name='delete_official'),

    path('staff-list/',views.WorkerListView.as_view(),name="workers_list"),
    path('register-staff/', views.WorkerRegisterView.as_view(), name='register_worker'),
    path('edit-staff/<int:pk>', views.WorkerUpdateView.as_view(), name='edit_worker'),
    path('delete-staff/<int:pk>', views.WorkerDeleteView.as_view(), name='delete_worker'),


    # path('water-cans/', views.watercan, name='watercan'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)