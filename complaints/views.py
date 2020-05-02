from django.shortcuts import redirect, render
from .models import Complaints
from institute.models import Institutestd, Officials
from django.http.response import Http404
from django.contrib import messages
from complaints.models import OfficialComplaints

# Create your views here.
def registerComplaint(request):
    if request.method == 'POST':
        if request.COOKIES.get('username_std'):
            user = Institutestd.objects.get(regd_no=request.COOKIES['username_std'])
            if request.POST.get('complainee'):
                newComplaint = Complaints(
                regd_no = user,
                type = request.POST['type'],
                complainee =  Institutestd.objects.get(regd_no=request.POST['complainee']),
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )
            else:
                newComplaint = Complaints(
                regd_no = user,
                type = request.POST['type'],
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )
        elif request.COOKIES.get('username_off'):
            user = Officials.objects.get(emp_id=request.COOKIES['username_off'])
            if request.POST.get('complainee'):
                newComplaint = OfficialComplaints(
                regd_no = user,
                type = request.POST['type'],
                complainee =  Institutestd.objects.get(regd_no=request.POST['complainee']),
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )
            else:
                newComplaint = OfficialComplaints(
                regd_no = user,
                type = request.POST['type'],
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )

        else:
            raise Http404('Please Log In and then register complaint!')
        


        newComplaint.save()
        messages.success(request, 'Complaint Registered Successfully!')
        redirect('complaints:registerComplaint')

    return render(request, 'complaints/complaint.html')