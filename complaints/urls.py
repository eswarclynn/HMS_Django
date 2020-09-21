from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .models import MedicalIssue, Complaint
from .forms import ComplaintCreationForm, MedicalIssueUpdationForm, ComplaintUpdationForm

app_name= 'complaints'

urlpatterns = [
    path('complaint/new/', views.ComplaintCreateView.as_view(model = Complaint, form_class = ComplaintCreationForm), name='registerComplaint'),
    path('complaint/<int:pk>/', views.ComplaintDetailView.as_view(model = Complaint), name='complaint_detail'),
    path('complaint/<int:pk>/edit', views.ComplaintUpdateView.as_view(model = Complaint, form_class = ComplaintUpdationForm), name='complaint_edit'),
    path('complaint/<int:pk>/delete', views.ComplaintDeleteView.as_view(model = Complaint), name='complaint_delete'),
    path('medical/new/', views.ComplaintCreateView.as_view(model = MedicalIssue, fields = ['summary', 'detailed']), name='registerMedical'),
    path('medical/<int:pk>/', views.ComplaintDetailView.as_view(model = MedicalIssue), name='medicalissue_detail'),
    path('medical/<int:pk>/edit', views.ComplaintUpdateView.as_view(model = MedicalIssue, form_class = MedicalIssueUpdationForm), name='medicalissue_edit'),
    path('medical/<int:pk>/delete', views.ComplaintDeleteView.as_view(model = MedicalIssue), name='medicalissue_delete'),
]