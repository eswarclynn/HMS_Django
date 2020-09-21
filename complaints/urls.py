from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name= 'complaints'

urlpatterns = [
    path('new/', views.ComplaintCreateView.as_view(), name='registerComplaint'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint_detail'),
    path('<int:pk>/edit', views.ComplaintUpdateView.as_view(), name='complaint_edit'),
    path('<int:pk>/delete', views.ComplaintDeleteView.as_view(), name='complaint_delete'),
]