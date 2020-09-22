from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from workers.models import Worker
from institute.models import Block, Student, Official
from complaints.models import Complaint, MedicalIssue
from students.models import RoomDetail
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required

def worker_check(user):
    return user.is_authenticated and user.is_worker

# Create your views here.
@user_passes_test(worker_check)
def home(request):
    user = request.user
    worker = user.worker    

    if worker.designation == 'Electrician':
        complaints = Complaint.objects.filter(type='Electrical', status='Registered') | Complaint.objects.filter(type='Electrical', status='Processing')
    if worker.designation == 'Mess Incharge':
        complaints = Complaint.objects.filter(type='Food Issues', status='Registered') | Complaint.objects.filter(type='Food Issues', status='Processing')
    if worker.designation == 'Doctor':
        complaints = MedicalIssue.objects.filter(status='Registered')

    return render(request, 'workers/home.html', {'worker': worker, 'complaints': complaints,})
