from django.urls import path

from . import views

app_name= 'students'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('outings', views.OutingListView.as_view(), name='outing_list'),
    path('outing/new', views.OutingCreateView.as_view(), name='outing_new'),
    path('outing/<int:pk>/edit', views.OutingUpdateView.as_view(), name='outing_edit'),
    path('attendance_history', views.attendance_history, name='attendance_history'),
]