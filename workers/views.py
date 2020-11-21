from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from workers.models import Worker
from complaints.models import Complaint, MedicalIssue
from django.contrib.auth.decorators import user_passes_test, login_required

def worker_check(user):
    return user.is_authenticated and user.is_worker

# Create your views here.
@user_passes_test(worker_check)
def home(request):
    user = request.user
    worker = user.worker    

    if worker.designation == 'Electrician':
        complaints = Complaint.objects.filter(type='Electrical', status__in=['Registered', 'Processing'])
    elif worker.designation == 'Estate Staff':
        complaints = Complaint.objects.filter(type=['Electrical', 'Civil'], status__in=['Registered', 'Processing'])
    elif worker.designation == 'Mess Incharge':
        complaints = Complaint.objects.filter(type='Food Issues', status__in=['Registered', 'Processing'])
    elif worker.designation == 'Doctor':
        complaints = MedicalIssue.objects.filter(status='Registered')
    else:
        raise PermissionDenied

    return render(request, 'workers/home.html', {'worker': worker, 'complaints': complaints,})
