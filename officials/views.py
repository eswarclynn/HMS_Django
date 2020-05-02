from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from institute.models import Blocks, Institutestd, Officials
from students.models import attendance as ATT
from students.models import details
from students.models import attendance
from students.models import outing as OUTINGDB
from django.contrib import messages
from datetime import date as datePy
from django.http.response import Http404
from complaints.models import Complaints, OfficialComplaints

# Create your views here.
@csrf_exempt
def official_home(request):
    name = request.COOKIES['username_off']
    user_details = Officials.objects.get(emp_id=str(name))
    if(user_details.designation == 'Caretaker' or user_details.designation == 'Warden'):
        try:
            block_details = Blocks.objects.get(emp_id_id=str(name))
        except Blocks.DoesNotExist:
            raise Http404("You are currently not appointed any block!")

        students = details.objects.filter(block_id=block_details.block_id)
    
        present_list = list()
        absent_list = list()
        for student in students:
            if ATT.objects.get(regd_no_id=student.regd_no_id).status == 'Present':
                present_list.append(
                    {
                        'block':student,
                        'info':Institutestd.objects.get(regd_no=str(student.regd_no))
                    }
                )
            elif ATT.objects.get(regd_no_id=student.regd_no_id).status == 'Absent':
                absent_list.append(
                    {
                        'block':student,
                        'info':Institutestd.objects.get(regd_no=str(student.regd_no))
                    }
                )

        complaints = list(Complaints.objects.filter(status='Registered'))

        if request.method == 'POST':
            for item in complaints:
                newComplaint = Complaints.objects.get(id=item.id)
                newComplaint.status = request.POST[str(item.id)]
                newComplaint.save()
            else:
                messages.success(request, 'Successfully Complaints updated!')
                return redirect('officials:official_home') 

        return render(request, 'officials/caretaker-home.html', {'user_details': user_details, 'block_details':block_details,'present_list':present_list,'absent_list':absent_list, 'complaints':complaints})

    else:
        name = request.COOKIES['username_off']
        user_details = Officials.objects.get(emp_id=str(name))
        pres = attendance.objects.filter(status='Present')
        present=list()
        for item in pres:
            present.append({
                'info':Institutestd.objects.get(regd_no=str(item.regd_no)),
                'block':details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))),
                'block_name': Blocks.objects.get(block_id=details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))).block_id_id).block_name
            })

        abse = attendance.objects.filter(status='Absent')
        absent=list()
        for item in abse:
            absent.append({
                'info':Institutestd.objects.get(regd_no=str(item.regd_no)),
                'block':details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))),
                'block_name': Blocks.objects.get(block_id=details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))).block_id_id).block_name

            })
        complaints = list(Complaints.objects.all())
        offComplaints = list(OfficialComplaints.objects.all())
        complaints+=offComplaints

        if request.method == 'POST':
            for item in complaints:
                newComplaint = Complaints.objects.get(id=item.id)
                newComplaint.status = request.POST[str(item.id)]
                newComplaint.save()
            else:
                messages.success(request, 'Successfully Complaints updated!')
                return redirect('officials:official_home')

        return render(request, 'officials/chiefs-home.html', {'user_details': user_details, 'present':present, 'absent':absent, 'complaints':complaints})



def profile(request):
    name = request.COOKIES['username_off']
    user_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.filter(emp_id_id=str(name))
    complaints=user_details.offComplaints.all()

    return render(request, 'officials/profile.html', {'user_details': user_details,'block_details':block_details, 'complaints':complaints})

def chiefsProfile(request):
    name = request.COOKIES['username_off']
    user_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.filter(emp_id_id=str(name))
    complaints=user_details.offComplaints.all()

    return render(request, 'officials/chiefs-profile.html', {'user_details': user_details, 'complaints':complaints})

@csrf_exempt
def takeAttendance(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.get(emp_id_id=str(name))
    students = details.objects.filter(block_id=block_details.block_id)
    
    stud_list = list()
    for student in students:
        stud_list.append(
            {
                'student':student,
                'name':Institutestd.objects.get(regd_no=str(student.regd_no)).name,
            }
        )

    if request.method == 'POST':
        date=request.POST["datefield"]
        attendance_list=list()
        for stud in stud_list:
            attendance_list.append(request.POST[str(stud['student'].regd_no)]) # Storing attendance for verification
            if (request.POST[str(stud['student'].regd_no)] == 'Present'):
                current = ATT.objects.get(regd_no_id=str(stud['student'].regd_no))
                currAtt = current.dates
                if currAtt == '':
                    currAtt += date
                else:
                    currAtt += (','+date)

                if current.status == '':
                    current.status = 'Present'
                else:
                    today = datePy.today()
                    if(date == str(today)):
                        current.status = 'Present'

                current.dates = currAtt
                current.save()
            else:
                current = ATT.objects.get(regd_no_id=str(stud['student'].regd_no))
                currAtt = current.dates
                if currAtt == '':
                    currAtt += ('X'+date)
                else:
                    currAtt += (',X'+date)

                if current.status == '':
                    current.status = 'Absent'
                else:
                    today = datePy.today()
                    if(date == str(today)):
                        current.status = 'Absent'
                
                current.dates = currAtt
                current.save()

        else:
            messages.success(request, f'Attendance marked for the date: {date}')
            return redirect('officials:attendance') 


    return render(request, 'officials/attendance.html', {'off_details':off_details, 'block_details':block_details, 'stud_list':stud_list})

def grantOuting(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.get(emp_id_id=str(name))
    students = details.objects.filter(block_id=block_details.block_id)

    stud_list = list()
    for student in students:
        outings = OUTINGDB.objects.filter(regd_no_id=str(student.regd_no), permission='Pending')
        for outing in outings:
            stud_list.append(
                {
                    'outing': outing,
                    'info':Institutestd.objects.get(regd_no=str(student.regd_no)),
                }
            )


    if request.method == 'POST':
        for stud in stud_list:
            if request.POST[str(stud['outing'].id)] !='':
                updateOuting = OUTINGDB.objects.get(id=stud['outing'].id)
                updateOuting.permission = request.POST[str(stud['outing'].id)]
                updateOuting.save()
        else:
            messages.success(request, 'Selected Outing requests updated!')
            return redirect('officials:grantOuting') 

    return render(request, 'officials/outingPending.html', {'off_details':off_details, 'stud_list':stud_list})



def search(request):
    
    return render(request, 'officials/search.html')