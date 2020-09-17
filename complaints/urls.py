from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name= 'complaints'

urlpatterns = [
    path('new/', login_required(views.registerComplaint), name='registerComplaint'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint_detail'),
]