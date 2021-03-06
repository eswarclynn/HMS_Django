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
from workers.models import Medical, Workers
from workers.models import attendance as ATTWORKER
from django.db.models import QuerySet
from officials.models import WaterCan
from django.db.models import Sum
from authenticate.models import credentials
import re
from officials.forms import PostForm


# Create your views here.
@csrf_exempt
def official_home(request):
    name = request.COOKIES['username_off']
    user_details = Officials.objects.get(emp_id=str(name))
    if(user_details.designation == 'Caretaker' or user_details.designation == 'Warden'):
        try:
            block_details = Blocks.objects.get(emp_id_id=str(name))
        except Blocks.DoesNotExist:
            raise Http404("You are currently not appointed any block! Please contact Admin")

        students = details.objects.filter(block_id=block_details.block_id)
        stud_roll = []
        for stud in students:
            stud_roll.append(stud.regd_no)
    
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

        complaints = list(Complaints.objects.filter(status='Registered', regd_no__in=stud_roll)) + list(Complaints.objects.filter(status='Processing', regd_no__in=stud_roll))

        if request.method == 'POST':
            for i in request.POST:
                if i == 'update':
                    comp_id = request.POST[i]
                    newComplaint = Complaints.objects.get(id=comp_id)
                    if newComplaint.status != request.POST[comp_id] or newComplaint.remark != request.POST['RE'+comp_id]:
                        newComplaint.status = request.POST[comp_id]
                        newComplaint.remark = request.POST['RE'+comp_id]
                        newComplaint.save()
                        messages.success(request, 'Successfully Updated Complaint ID:'+str(newComplaint.id)+'!')
                        return redirect('officials:official_home') 

        return render(request, 'officials/caretaker-home.html', {'user_details': user_details, 'block_details':block_details,'present_list':present_list,'absent_list':absent_list, 'complaints':complaints})

    else:
        name = request.COOKIES['username_off']
        user_details = Officials.objects.get(emp_id=str(name))
        pres = attendance.objects.filter(status='Present')
        present=list()
        for item in pres:
            try:
                present.append({
                    'info':Institutestd.objects.get(regd_no=str(item.regd_no)),
                    'block':details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))),
                    'block_name': Blocks.objects.get(block_id=details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))).block_id_id).block_name
                })
            except: pass

        abse = attendance.objects.filter(status='Absent')
        absent=list()
        for item in abse:
            try:
                absent.append({
                    'info':Institutestd.objects.get(regd_no=str(item.regd_no)),
                    'block':details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))),
                    'block_name': Blocks.objects.get(block_id=details.objects.get(regd_no = Institutestd.objects.get(regd_no=str(item.regd_no))).block_id_id).block_name
                })
            except: pass

        complaints = list(Complaints.objects.filter(status='Registered')) + list(Complaints.objects.filter(status='Processing'))
        offComplaints = list(OfficialComplaints.objects.filter(status='Registered')) + list(OfficialComplaints.objects.filter(status='Processing'))
        complaints_list = complaints + offComplaints
        if request.method == 'POST':
            for i in request.POST:
                if i == 'SCupdate':
                    comp_id = request.POST[i]
                    newComplaint = Complaints.objects.get(id=comp_id)
                    if newComplaint.status != request.POST['SC'+comp_id] or newComplaint.remark != request.POST['SCRE'+comp_id]:
                        newComplaint.status = request.POST['SC'+comp_id]
                        newComplaint.remark = request.POST['SCRE'+comp_id]
                        newComplaint.save()
                        messages.success(request, 'Successfully Updated Complaint ID:'+str(newComplaint.id)+'!')
                        return redirect('officials:official_home') 

                if i == 'OCupdate':
                    comp_id = request.POST[i]
                    newComplaint = OfficialComplaints.objects.get(id=comp_id)
                    if newComplaint.status != request.POST['OC'+comp_id] or newComplaint.remark != request.POST['OCRE'+comp_id]:
                        newComplaint.status = request.POST['OC'+comp_id]
                        newComplaint.remark = request.POST['OCRE'+comp_id]
                        newComplaint.save()
                        messages.success(request, 'Successfully Updated Complaint ID:'+str(newComplaint.id)+'!')
                        return redirect('officials:official_home') 

        return render(request, 'officials/chiefs-home.html', {'user_details': user_details, 'present':present, 'absent':absent, 'complaints':complaints,'complaints_list':complaints_list , 'offComplaints':offComplaints})



def profile(request):
    name = request.COOKIES['username_off']
    user_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.filter(emp_id_id=str(name))
    complaints=list(user_details.offComplaints.filter(status='Registered')) + list(user_details.offComplaints.filter(status='Processing'))

    return render(request, 'officials/profile.html', {'user_details': user_details,'block_details':block_details, 'complaints':complaints})

def chiefsProfile(request):
    name = request.COOKIES['username_off']
    user_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.filter(emp_id_id=str(name))
    complaints=list(user_details.offComplaints.filter(status='Registered')) + list(user_details.offComplaints.filter(status='Processing'))

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
                'info':Institutestd.objects.get(regd_no=str(student.regd_no)),
            }
        )

    if request.method == 'POST':
        if request.POST.get('submit'):
            print('taking attendance')
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
                        pos = currAtt.find(date)
                        if pos != -1:
                            if currAtt[pos-1] == 'X':
                                currAtt = currAtt[:pos-1]+currAtt[pos:]
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
                        pos = currAtt.find(date)
                        if pos != -1:
                            if currAtt[pos-1] != 'X':
                                currAtt = currAtt[:pos]+'X'+currAtt[pos:]
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

        if request.POST.get('get_date'):
            get_date = request.POST.get('get_date')
            for stud in stud_list:
                pos = stud['info'].attendance.dates.find(get_date)
                if pos != -1:
                    if stud['info'].attendance.dates[pos-1] == 'X':
                        stud['att'] = 'Absent'
                    else:
                        stud['att'] = 'Present'
            return render(request, 'officials/attendance.html', {'off_details':off_details, 'block_details':block_details, 'stud_list':stud_list, 'get_date':get_date})
              

    return render(request, 'officials/attendance.html', {'off_details':off_details, 'block_details':block_details, 'stud_list':stud_list})


@csrf_exempt
def attendance_workers(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.get(emp_id_id=str(name))
    students = Workers.objects.filter(block=block_details.block_id)
    
    stud_list = list()
    for student in students:
        stud_list.append(
            {
                'student':student,
            }
        )

    if request.method == 'POST':
        if request.POST.get('submit'):
            print('taking attendance')
            date=request.POST["datefield"]
            attendance_list=list()
            for stud in stud_list:
                attendance_list.append(request.POST[str(stud['student'].staff_id)]) # Storing attendance for verification
                if (request.POST[str(stud['student'].staff_id)] == 'Present'):
                    current = ATTWORKER.objects.get(staff_id=str(stud['student'].staff_id))
                    currAtt = current.dates
                    if currAtt == '':
                        currAtt += date
                    else:
                        pos = currAtt.find(date)
                        if pos != -1:
                            if currAtt[pos-1] == 'X':
                                currAtt = currAtt[:pos-1]+currAtt[pos:]
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
                    current = ATTWORKER.objects.get(staff_id=str(stud['student'].staff_id))
                    currAtt = current.dates
                    if currAtt == '':
                        currAtt += ('X'+date)
                    else:
                        pos = currAtt.find(date)
                        if pos != -1:
                            if currAtt[pos-1] != 'X':
                                currAtt = currAtt[:pos]+'X'+currAtt[pos:]
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
                return redirect('officials:attendance_workers')

        if request.POST.get('get_date'):
            get_date = request.POST.get('get_date')
            for stud in stud_list:
                pos = stud['student'].attendance.dates.find(get_date)
                if pos != -1:
                    if stud['student'].attendance.dates[pos-1] == 'X':
                        stud['att'] = 'Absent'
                    else:
                        stud['att'] = 'Present'
            return render(request, 'officials/attendance-workers.html', {'off_details':off_details, 'block_details':block_details, 'stud_list':stud_list, 'get_date':get_date})
              

    return render(request, 'officials/attendance-workers.html', {'off_details':off_details, 'block_details':block_details, 'stud_list':stud_list})



def attendance_log(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    try:
        block_details = Blocks.objects.get(emp_id_id=str(name))
        stud_set = block_details.details_set.all()
    except:
        block_details = None

    if request.method == 'POST':
        if(request.POST["date"]):
            date=request.POST["date"]
            if block_details:
                studs = list()
                for item in stud_set:
                    studs += ATT.objects.filter(regd_no_id=item.regd_no_id)

            else:   studs = ATT.objects.all()

            pres_stud = list()
            abse_stud = list()
            for stud in studs:
                att = str(stud.dates)
                try:
                    pos = att.index(date)
                    if att[pos-1] == 'X':
                        abse_stud.append({
                            'info': Institutestd.objects.get(regd_no=stud.regd_no_id),
                            'block': details.objects.get(regd_no=stud.regd_no_id)
                            })
                    else: 
                        pres_stud.append({
                            'info': Institutestd.objects.get(regd_no=stud.regd_no_id),
                            'block': details.objects.get(regd_no=stud.regd_no_id)
                            })
                except ValueError:
                    pos = -1
            if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
                return render(request, 'officials/attendance-log-chief.html', {'off_details':off_details, 'block_details':block_details, 'pres_stud':pres_stud, 'abse_stud':abse_stud})
            else:
                return render(request, 'officials/attendance-log.html', {'off_details':off_details, 'block_details':block_details, 'pres_stud':pres_stud, 'abse_stud':abse_stud})


        elif(request.POST["regno"]):
            regno = request.POST["regno"]
            if not Institutestd.objects.get(regd_no=str(regno)).exists():
                messages.error(request, 'Invalid Student Roll No.')
                return redirect('officials:attendance_log')
            user_details = Institutestd.objects.get(regd_no=str(regno))
            current = attendance.objects.get(regd_no_id=regno).dates
            dates = current.split(',')
            abse = list(filter(lambda x: (x.startswith('X')), dates))
            pres = list(filter(lambda x: not (x.startswith('X')), dates))
            abse = list(map(lambda x: x.replace('X',''), abse))

            if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
                return render(request, 'officials/attendance-log-chief.html', {'off_details':off_details, 'block_details':block_details, 'pres_dates':pres, 'abse_dates':abse})
            else:
                return render(request, 'officials/attendance-log.html', {'off_details':off_details, 'block_details':block_details, 'pres_dates':pres, 'abse_dates':abse})

            
    if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
        return render(request, 'officials/attendance-log-chief.html', {'off_details':off_details, 'block_details':block_details,})
    else:
        return render(request, 'officials/attendance-log.html', {'off_details':off_details, 'block_details':block_details,})


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
        for i in request.POST:
            if i == 'HIS':
                user_details = Institutestd.objects.get(regd_no=str(request.POST[i]))
                outing_details = OUTINGDB.objects.filter(regd_no=str(request.POST[i]))
                return render(request, 'officials/outingHisto.html', {'user_details': user_details, 'outing_details':outing_details})
            if i == 'GR':
                updateOuting = OUTINGDB.objects.get(id=str(request.POST[i]))
                updateOuting.permission = 'Granted'
                updateOuting.save()
                messages.success(request, 'Granted Outing permission to '+updateOuting.regd_no.name+'!')
                return redirect('officials:grantOuting')

            if i == 'RE':
                updateOuting = OUTINGDB.objects.get(id=str(request.POST[i]))
                updateOuting.permission = 'Rejected'
                updateOuting.save()
                messages.success(request, 'Rejected Outing permission to '+updateOuting.regd_no.name+'!')
                return redirect('officials:grantOuting')

    return render(request, 'officials/outingPending.html', {'off_details':off_details, 'stud_list':stud_list})


@csrf_exempt
def search(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
        send_blocks = Blocks.objects.all()
        if request.method == 'POST':
            if request.POST.get('regno'):
                stud = Institutestd.objects.get(regd_no=str(request.POST.get('regno')))
                block_details = details.objects.get(regd_no=stud)
                block = Blocks.objects.get(block_id=block_details.block_id_id)
                if attendance.objects.get(regd_no=stud).status=='':isPresent = 'Absent'
                else: isPresent = attendance.objects.get(regd_no=stud).status
                items={
                    'stud':stud,
                    'block_details':block_details,
                    'block_name':block.block_name,
                    'isPresent':isPresent
                }
                items_list = list()
                items_list.append(items)

                return render(request, 'officials/search.html', {'items_list':(items_list), 'send_blocks':send_blocks})

            else:
                block_name = Blocks.objects.get(block_id=request.POST['block']).block_name
                studs = details.objects.filter(block_id=request.POST['block'])
                items_list = list()
                for stud in studs:
                    info = Institutestd.objects.get(regd_no=str(stud.regd_no_id))
                    block_details = details.objects.get(regd_no=info)
                    if attendance.objects.get(regd_no=info).status=='':isPresent = 'Absent'
                    else: isPresent = attendance.objects.get(regd_no=info).status
                    items={
                        'stud':info,
                        'block_details':block_details,
                        'block_name':block_name,
                        'isPresent':isPresent
                    }
                    items_list.append(items)
                return render(request, 'officials/search.html', {'items_list':(items_list), 'send_blocks':send_blocks})

        return render(request, 'officials/search.html',{'send_blocks':send_blocks})

@csrf_exempt
def blockSearch(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
        send_blocks = Blocks.objects.all()
        if request.POST.get('submit'):
            block_name = Blocks.objects.get(block_id=request.POST['block']).block_name
            block_gender = Blocks.objects.get(block_id=request.POST['block']).gender
            block_care = Blocks.objects.get(block_id=request.POST['block']).emp_id_id
            cap_room = (Blocks.objects.get(block_id=request.POST['block']).capacity)
            room_type = Blocks.objects.get(block_id=request.POST['block']).room_type
            block_name_lower = Blocks.objects.get(block_id=request.POST['block']).block_name.lower()
            print(block_name_lower)
            
            if room_type == '4S':   cap_stud = cap_room*4
            elif room_type == '2S': cap_stud = cap_room*2
            elif room_type == '1S': cap_stud = cap_room
            
            studs = details.objects.filter(block_id=request.POST['block'])
            pres_stud = studs.count()
            items_list = list()
            for stud in studs:
                info = Institutestd.objects.get(regd_no=str(stud.regd_no_id))
                block_details = details.objects.get(regd_no=info)
                if attendance.objects.get(regd_no=info).status=='':isPresent = 'Absent'
                else: isPresent = attendance.objects.get(regd_no=info).status
                items={
                    'stud':info,
                    'block_details':block_details,
                    'isPresent':isPresent
                }
                items_list.append(items)
    
            return render(request, 'officials/roomLayout.html', {
                'items_list':(items_list), 
                'send_blocks':send_blocks, 
                'block_name':block_name,
                'cap_room': cap_room,
                'room_type' : room_type,
                'cap_stud' : cap_stud,
                'block_gender':block_gender,
                'block_care':block_care,
                'pres_stud':pres_stud,
                'pres_room': (int(pres_stud))//(int(room_type[0])),
                'vacant_room':cap_room - (int(pres_stud))//(int(room_type[0])) - (int(pres_stud))%(int(room_type[0])),
                'partial_room':(int(pres_stud))%(int(room_type[0])),
                'block_name_lower':block_name_lower
                })
    
        if request.POST.get('Add'):
            roll = (request.POST.get('roll'))
            location = (request.POST.get('room')).split('-')
            placing_block = location[0]
            placing_floor = location[1]
            placing_room = location[2]
            print(placing_block)
    
            if details.objects.filter(regd_no=roll).exists():
                student = details.objects.get(regd_no=roll)
                if student.block_id_id != None and student.room_no != None and student.floor != None:
                    messages.error(request, 'Student : '+str(roll)+' already alloted room!')
                    return redirect('officials:blockSearch')
                else:
                    block_req = Blocks.objects.get(block_name=placing_block)
                    stud_req = Institutestd.objects.get(regd_no=roll)
                    if (stud_req.gender == block_req.gender) and ((stud_req.year == 1 and block_req.room_type == '4S') or (stud_req.year == 2 and block_req.room_type == '2S') or (stud_req.year == 3 and block_req.room_type == '2S') or (stud_req.year == 4 and block_req.room_type == '1S')):
                        student.block_id = Blocks.objects.get(block_name=placing_block)
                        student.room_no = int(placing_room)
                        student.floor = placing_floor
    
                        student.save()
                        messages.success(request,'Student : '+str(roll)+' alloted room '+student.floor+'-'+str(student.room_no)+' in block '+str(student.block_id_id)+' : '+placing_block+'!')
                        return redirect('officials:blockSearch')
                    else:
                        messages.error(request, 'Incompatible Block for Student with roll no. : '+str(roll)+'!')
                        return redirect('officials:blockSearch')
    
    
            else:
                messages.error(request, 'No Student with roll no. : '+str(roll)+' found!')
                return redirect('officials:blockSearch')
    
        if request.POST.get('change'):
            block_name = request.POST.get('block')
            block_req = Blocks.objects.get(block_name=block_name)
            studs = details.objects.filter(block_id=block_req)
            for stud in studs:
                if request.POST.get(str(stud.regd_no)):
                    if request.POST.get(str(stud.regd_no)) == 'None':
                        stud.block_id = None
                        stud.room_no = None
                        stud.floor = None
                        stud.save()
    
                        messages.success(request, 'Student : '+str(stud.regd_no)+' removed from block : '+block_name+'!')
                        return redirect('officials:blockSearch')
    
    
                    else:
                        roll = request.POST.get(str(stud.regd_no))
                        stud_req = Institutestd.objects.get(regd_no=roll)
                        student = details.objects.get(regd_no=roll)
                        if (stud_req.gender == block_req.gender) and ((stud_req.year == 1 and block_req.room_type == '4S') or (stud_req.year == 2 and block_req.room_type == '2S') or (stud_req.year == 3 and block_req.room_type == '2S') or (stud_req.year == 4 and block_req.room_type == '1S')):
                            student.block_id = stud.block_id
                            student.room_no = stud.room_no
                            student.floor = stud.floor
                            student.save()
    
                            stud.block_id = None
                            stud.room_no = None
                            stud.floor = None
                            stud.save()
    
                            messages.success(request,'Student : '+str(roll)+' alloted room '+student.floor+'-'+str(student.room_no)+' in block '+str(student.block_id_id)+' : '+block_name+'!')
                            messages.success(request, 'Student : '+str(stud.regd_no)+' removed from block : '+block_name+'!')
                            return redirect('officials:blockSearch')
                        else:
                            messages.error(request, 'Incompatible Block for Student with roll no. : '+str(roll)+'!')
                            return redirect('officials:blockSearch')
    
    
    
        return render(request, 'officials/roomLayout.html',{'send_blocks':send_blocks})




    

def register (request):
    if request.method == 'POST':
        # print(request.POST)
        print(request.FILES)
        if request.POST.get("submit"):
            form=PostForm(request.POST,request.FILES)
            regdno=request.POST["regno"]
            rollno=request.POST["rollno"]
            name=request.POST["name"]
            year=request.POST["year"]
            branch=request.POST["branch"]
            gender=request.POST["type"]
            print(gender)
            pwd=request.POST["pwd"]
            print(pwd)
            cast=request.POST["caste"]
            dob=request.POST["dob"]
            print("hi")
            print(type(dob))
            bgp=request.POST["blood"]
            email=request.POST["email"]
            ph_std=request.POST["ph_std"]
            ph_p=request.POST["ph_p"]
            ph_emr=request.POST["ph_emr"]
            address=request.POST["address"]
            photo=request.FILES["photo"]
            hosteller=request.POST["hosteller"]
            if pwd =="Yes":
                 pwd='Y'
            else :
                 pwd='N'
            try :
                amount=request.POST["amount"]
                bank=request.POST["bank"]
                ch_no=request.POST["ch_no"]
                dop=request.POST['dop']
                appli=request.FILES["application"]
                undertake=request.FILES["undertake"]
                recipt=request.FILES["recipt"]
            except :
                 amount=None
                 bank=None
                 ch_no=None
                 dop=None
                 appli=None
                 undertake=None
                 recipt=None
            try :
                    afd=request.FILES["afd"]
            except :
                    afd=None

               
            if hosteller == "H":
                    hosteller="Y"
            else:
                hosteller="N"
            
            if Institutestd.objects.filter(regd_no=regdno).exists():
                messages.error(request, 'Student already registered. Details will be updated!')
                sstd=Institutestd.objects.filter(regd_no=regdno).delete()

            temp="N"
            if amount !=None and hosteller == "Y":
                temp="Y"
            if hosteller == "N": #bank == None and ch_no == None and dop==None and appli ==None and undertake ==None and recipt == None:
                 bank="null"
                 ch_no="null"
                 dop= None
                 appli="null"
                 undertake="null"
                 recipt="null"
            elif hosteller == "Y": #bank != None and ch_no != None and dop!=None and appli !=None and undertake !=None and recipt != None and afd==None:
                 afd="null"
            else :
                 messages.error(request, 'Invalid Registration!')
                 return redirect('officials:register')
            acc = form.save(commit=False)
            #acc=Institutestd(regdno,rollno,name,branch,gender,pwd,cast,year,dob,bgp,email,ph_std,ph_p,ph_emr,address,photo,hosteller,amount,bank,ch_no,dop,appli,undertake,recipt,afd,temp)
            acc.regd_no=regdno
            acc.roll_no=rollno
            acc.name=name
            acc.branch=branch
            acc.gender=gender
            acc.pwd=pwd
            acc.caste=cast
            acc.year=year
            acc.dob=dob
            acc.bgp=bgp
            acc.email_id=email
            acc.phone=ph_std
            acc.ph_phone=ph_p
            acc.emr_phone=ph_emr
            acc.address=address
            acc.hosteller=hosteller
            acc.amount=amount
            acc.bank=bank
            acc.ch_no=ch_no
            acc.dop=dop
            acc.paid=temp
            
                    
            acc.save()
            print(acc)
            messages.success(request, ' Registration Successful!')
            return redirect('officials:register')

    return render(request,'officials/register.html',{})

def registeremp (request):
    std=Blocks.objects.all()
    if request.method == 'POST':
        if request.POST.get("submit_btn"):
            empid=request.POST["empid"]
            name=request.POST["name"]
            desig=request.POST['desig']
            gender=request.POST["type"]
            email=request.POST["email"]
            ph=request.POST['ph']
            block_id=request.POST['block']
            branch=request.POST['branch']
            
            
            if Officials.objects.filter(emp_id=empid).exists():
                messages.error(request, 'Employee Already Registered! Details will be updated.')
                temp=Officials.objects.get(emp_id=empid)
                try:
                    b=Blocks.objects.get(emp_id=temp)
                    b.emp_id=None
                    b.save()
                except: pass
                Officials.objects.get(emp_id=empid).delete()
                  
            acc=Officials(empid,name,desig,branch,ph,email)
            acc.save()
            if block_id!="null":
                em=Blocks.objects.get(block_id=block_id)
                print(em)
                if em.emp_id :
                     messages.error(request,"Block assigned to another official. Will be assigned to current official now!")
                     em.emp_id=Officials.objects.get(emp_id=empid)
                     em.save()
                else:
                     em.emp_id=Officials.objects.get(emp_id=empid)
                     em.save()
            messages.success(request, 'Registration Successful!')
    return render(request,'officials/register-emp.html',{'std':std,})

     

def student_list(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
        students=Institutestd.objects.all()
        list_of_students=list()
        for stud in students :
            x=details.objects.filter(regd_no=stud)
            try :
                block_id=str(details.objects.get(regd_no=str(stud.regd_no)).block_id)
                block=int(re.search(r'\d+', block_id).group(0))
                print(stud.gender)
                list_of_students.append({
                    'regd_no':str(stud.regd_no),
                    'name':stud.name,
                    'ph':str(stud.phone),
                    'year':str(stud.year),
                    'branch':str(stud.branch),
                    'gender':str(stud.gender),
                    'floor':details.objects.get(regd_no=str(stud.regd_no)).floor,
                    'room_no':details.objects.get(regd_no=str(stud.regd_no)).room_no,
                    'block_id':details.objects.get(regd_no=str(stud.regd_no)).block_id,
                    'block':Blocks.objects.get(block_id=str(block)).block_name,

                })
                
            except:
                #messages.error(request,"No students are there!")
                list_of_students.append({
                    'regd_no':str(stud.regd_no),
                    'name':stud.name,
                    'ph':str(stud.phone),
                    'year':str(stud.year),
                    'branch':str(stud.branch),
                    'gender':str(stud.gender),
                    'floor':"None",
                    'room_no':"None",
                    'block_id':"None",
                    'block':"None",

                })
                
        return render(request,'officials/student_list.html',{'list_of_students':list_of_students})
def studentdelete (request):
    students=Institutestd.objects.all()
    if request.method=='POST':
        print(request.POST)
        for stud in students:
            if request.POST.get("d"+str(stud.regd_no)):
                print(stud.regd_no)
                try:
                    Institutestd.objects.get(regd_no=str(stud.regd_no)).delete()
                    #Institutestd.objects.get(regd_no=str(stud.regd_no)).delete()
                    credentials.objects.get(regd_no=str(stud.regd_no)).delete()
                    attendance.objects.get(regd_no=str(stud.regd_no)).delete()
                except:
                    pass
                messages.success(request,str(stud.regd_no)+" is deleted!")
                return redirect('officials:student_list')
            elif request.POST.get("e"+str(stud.regd_no)):
                #response=redirect('officials:register_edit')
                #response.set_cookie('regd_no_edit',str(stud.regd_no))
                #return response
                std=Institutestd.objects.get(regd_no=str(stud.regd_no))
                return render(request,'officials/register.html',{'std':std})

def emp_list(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
        emp=Officials.objects.all()
        list_of_emp=list()
        if emp == None:
            messages.error(request,"No officials are present!")
            return redirect("official:registeremp")
        for em in emp:
            print("came")
            try :
                block=Blocks.objects.get(emp_id=em).block_name
                list_of_emp.append({'block':block,'emp_id':em.emp_id,'name':em.name,'branch':em.branch,'desig':em.designation,'ph':em.phone,'email':em.email_id,})
            except:
                list_of_emp.append({'block':"",'emp_id':em.emp_id,'name':em.name,'branch':em.branch,'desig':em.designation,'ph':em.phone,'email':em.email_id,})
        return render(request,'officials/emp_list.html',{'emp':list_of_emp})
        
def empdelete (request):
    emp=Officials.objects.all()
    if request.method=='POST':
        print(request.POST)
        print("came in")
        for stud in emp:
            print("came in")
            print(stud.emp_id)
            if request.POST.get("d"+str(stud.emp_id)):
                print(stud.emp_id)
                Officials.objects.get(emp_id=str(stud.emp_id)).delete()
                #Institutestd.objects.get(regd_no=str(stud.regd_no)).delete()
                try:
                    credentials.objects.get(emp_id=str(stud.emp_id)).delete()
                    Blocks.objects.get(emp_id=stud).delete()
                except:
                    pass
                messages.success(request,str(stud.emp_id)+" is deleted!")
                return redirect('officials:emp_list')
            elif request.POST.get("e"+str(stud.emp_id)):
                #response=redirect('officials:register_edit')
                #response.set_cookie('regd_no_edit',str(stud.regd_no))
                #return response
                std=Blocks.objects.all()
                employee=Officials.objects.get(emp_id=str(stud.emp_id))
                try:
                    block=Blocks.objects.get(emp_id=employee)
                except:
                    block = None

                return render(request,'officials/register-emp.html',{'std':std,'employee':employee,'block':block})

def registerworker(request):
    work=Workers.objects.all()
    if request.method == 'POST':
        if request.POST.get("submit_btn"):
            print(request.POST)
            staff_id=request.POST["empid"]
            name=request.POST["name"]
            gender=request.POST["type"]
            desig=request.POST["desig"]
            email=request.POST["email"]
            phone=request.POST["ph"]
            block_id=request.POST["block"]
            print(block_id)
            try:
                block=int(re.search(r'\d+', block_id).group(0))
                #block=Blocks.objects.get(block_id=block)
            except: 
                block=None
            if Workers.objects.filter(staff_id=staff_id).exists():
                Workers.objects.filter(staff_id=staff_id).delete()
                messages.error(request,"Already staff registered. Details will be updated!")
            s=Workers(staff_id,name,desig,gender,phone,email,block)
            s.save()
            messages.success(request,"Successfully registered!")
    std=Blocks.objects.all()
    return render(request,"officials/register_staff.html",{'std':std})

def workers_list(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    if off_details.designation == 'Deputy Chief-Warden' or off_details.designation == 'Chief-Warden':
        worker=Workers.objects.all()
        if worker == None:
            messages.error(request,"Workers list is empty !")
            return render(request,"official/workerslist.html",{'emp':worker})
        list_of_emp=list()
        for em in worker:
            print("came in")
            try:
                
                block=Blocks.objects.get(block_id=em.block_id).block_name
            except:
                block="None"
                print(block)
            list_of_emp.append({
                'staff_id':em.staff_id,
                'name':em.name,
                'desig':em.designation,
                'gender':em.gender,
                'ph':em.phone,
                'block':block,
                
            })
        return render(request,"officials/workerslist.html",{'emp':list_of_emp})


def workerdelete (request):
    emp=Workers.objects.all()
    if request.method=='POST':
        print(request.POST)
        print("came in")
        for stud in emp:
            print("came in")
            print(stud.staff_id)
            if request.POST.get("d"+str(stud.staff_id)):
                print(stud.staff_id)
                Workers.objects.get(staff_id=str(stud.staff_id)).delete()
                #Institutestd.objects.get(regd_no=str(stud.regd_no)).delete()
                try:
                    credentials.objects.get(staff_id=str(stud.staff_id)).delete()
                    
                except:
                    pass
                messages.success(request,str(stud.staff_id)+" is deleted!")
                return redirect('officials:workers_list')
            elif request.POST.get("e"+str(stud.staff_id)):
                #response=redirect('officials:register_edit')
                #response.set_cookie('regd_no_edit',str(stud.regd_no))
                #return response
                std=Blocks.objects.all()
                employee=Workers.objects.get(staff_id=str(stud.staff_id))
                print(employee.block_id)
                try:
                    
                    block=Blocks.objects.get(block_id=str(employee.block_id)).block_name
                    
                except:
                    block="None"
                print(block)
                return render(request,'officials/register_staff.html',{'std':std,'employee':employee,'block':block})


@csrf_exempt
def watercan(request):
    name = request.COOKIES['username_off']
    off_details = Officials.objects.get(emp_id=str(name))
    block_details = Blocks.objects.get(emp_id_id=str(name))

    if request.method == 'POST':
        if request.POST.get('submit_btn'):
            date = request.POST.get('date')
            received = request.POST.get('received')
            given = request.POST.get('given')

            if WaterCan.objects.filter(block=block_details, date=date).exists():
                current = WaterCan.objects.get(block=block_details, date=date)
                current.received = received
                current.given = given
                current.save()
            else:
                newCan = WaterCan(block=block_details, date=date, received=received, given=given)
                newCan.save()
            messages.success(request, 'Water Cans Info updated')
            return redirect('officials:watercan')

        elif request.POST.get('count_btn'):
            if request.POST.get('date_hist'):
                date_hist = request.POST.get('date_hist')
                if WaterCan.objects.filter(block=block_details, date=date_hist).exists():
                    dateRec = WaterCan.objects.get(block=block_details, date=date_hist).received
                    dateGiven = WaterCan.objects.get(block=block_details, date=date_hist).given
                else:
                    dateRec = -10
                    dateGiven = -10
                return render(request, 'officials/water-can.html', {'dateRec':dateRec, 'dateGiven':dateGiven, 'dateUsed':dateGiven})

            elif request.POST.get('month_hist'):
                month = int(request.POST.get('month_hist').split('-')[1])
                if WaterCan.objects.filter(block=block_details, date__month=month).exists():
                    month_set = WaterCan.objects.filter(block=block_details, date__month=month).order_by('-date')
                    month_rec = month_set.aggregate(Sum('received'))['received__sum']
                    month_given = month_set.aggregate(Sum('given'))['given__sum']
                    month_used = month_given
                    return render(request, 'officials/water-can.html', {'month':request.POST.get('month_hist'), 'month_empty':False, 'month_set':month_set, 'month_rec':month_rec, 'month_given':month_given, 'month_used':month_used})
                else:
                    return render(request, 'officials/water-can.html', {'month_empty':True})



    return render(request, 'officials/water-can.html')