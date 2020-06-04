from django.shortcuts import redirect, render
from institute.models import Blocks, Institutestd, Officials
from students.models import attendance, outing
from django.http import HttpResponse
import datetime
from django.contrib import messages

# Create your views here.
def student_home(request):
    name = request.COOKIES['username_std']
    user_details = Institutestd.objects.get(regd_no=str(name))
    current = attendance.objects.get(regd_no_id=name).dates
    dates = current.split(',')
    abse = len(list(filter(lambda x: (x.startswith('X')), dates)))
    pres = len(list(filter(lambda x: not (x.startswith('X')), dates)))
    complaints=list(user_details.complaints.filter(status="Registered")) + list(user_details.complaints.filter(status="Processing"))

    return render(request, 'students/student-home.html', {'user_details': user_details, 'pres':pres, 'abse':abse, 'complaints':complaints})

def outing_app(request):
    if request.method == 'POST':
        reg_no = request.COOKIES['username_std']
        fromDate = request.POST['fromDate']
        fromTime = request.POST['fromTime']
        toDate = request.POST['toDate']
        toTime = request.POST['toTime']
        purpose = request.POST['purpose']
        parents_mobile = Institutestd.objects.get(regd_no=reg_no).ph_phone

        print(reg_no, fromDate, fromTime, toDate, toTime, purpose, parents_mobile)

        fromDateObj = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
        toDateObj = datetime.datetime.strptime(toDate, '%Y-%m-%d')
        fromTimeObj = datetime.datetime.strptime(fromTime, '%H:%M')
        toTimeObj = datetime.datetime.strptime(toTime, '%H:%M')

        application = outing(
            regd_no= Institutestd.objects.get(regd_no = reg_no),
            fromDate=fromDateObj,
            fromTime=fromTimeObj,
            toDate=toDateObj,
            toTime=toTimeObj,
            purpose=purpose,
            parent_mobile=parents_mobile
        )
        application.save()
        messages.success(request, 'Outing Application submitted successfully! Check Outing History for status')
        return redirect('students:outing_app')

    return render(request, 'students/OutingApp.html')

def attendance_history(request):
    reg_no = request.COOKIES['username_std']
    user_details = Institutestd.objects.get(regd_no=str(reg_no))
    current = attendance.objects.get(regd_no_id=reg_no).dates
    dates = current.split(',')
    abse = list(filter(lambda x: (x.startswith('X')), dates))
    pres = list(filter(lambda x: not (x.startswith('X')), dates))
    abse = list(map(lambda x: x.replace('X',''), abse))

    return render(request, 'students/attendance-history.html', {'user_details':user_details, 'pres':pres, 'abse':abse})

def outing_history(request):
    reg_no = request.COOKIES['username_std']
    user_details = Institutestd.objects.get(regd_no=str(reg_no))
    outing_details = outing.objects.filter(regd_no=str(reg_no))

    return render(request, 'students/outingHisto.html', {'user_details': user_details, 'outing_details':outing_details})

