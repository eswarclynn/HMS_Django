from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from institute.models import Block, Student, Official
from students.models import Attendance, RoomDetail, Outing as OUTINGDB
from django.contrib import messages
from datetime import date as datePy
from django.http.response import Http404
from complaints.models import Complaint
from workers.models import MedicalIssue, Worker, Attendance as AttendanceWorker
from django.db.models import QuerySet
from django.db.models import Sum
import re

def official_check(user):
    return user.is_authenticated and user.is_official


def chief_warden_check(user):
    if official_check(user):
        official = user.official
        chief_check = official.designation == 'Deputy Chief-Warden' or official.designation == 'Chief-Warden'
    return official_check(user) and chief_check


# Create your views here.
@user_passes_test(official_check)
@csrf_exempt 
def official_home(request):
    user = request.user
    official = user.official
    if official.is_chief():
        present_students = Attendance.objects.filter(status='Present')
        absent_students = Attendance.objects.filter(status='Absent')
        complaints = Complaint.objects.filter(status='Registered') | Complaint.objects.filter(status='Processing')

    else:
        try:
            block_details = official.block
        except Block.DoesNotExist:
            raise Http404('You are currently not appointed any block! Please contact Admin')

        student_rooms = RoomDetail.objects.filter(block=block_details)
        student_ids = student_rooms.values_list('student', flat=True)
        students = Student.objects.filter(pk__in=student_ids)
        present_students = Attendance.objects.filter(student__in=students, status='Present')
        absent_students = Attendance.objects.filter(student__in=students, status='Absent')
        complaints = Complaint.objects.filter(entity_id__in=students.values_list('regd_no', flat=True), status='Registered') | Complaint.objects.filter(entity_id__in=students.values_list('regd_no', flat=True), status='Processing')

    return render(request, 'officials/home.html', {'user_details': official, 'present':present_students, 'absent':absent_students, 'complaints':complaints,})




@user_passes_test(official_check)
def profile(request):
    user = request.user
    official = user.official
    complaints = Complaint.objects.filter(entity_id = official.emp_id)
    return render(request, 'officials/profile.html', {'official': official, 'complaints': complaints})

@user_passes_test(official_check)
@csrf_exempt
def takeAttendance(request):
    user = request.user
    user_details = Officials.objects.get(email_id = user.email)
    block_details = user_details.blocks
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
            return render(request, 'officials/attendance.html', {'off_details':user_details, 'block_details':block_details, 'stud_list':stud_list, 'get_date':get_date})
              

    return render(request, 'officials/attendance.html', {'off_details':user_details, 'block_details':block_details, 'stud_list':stud_list})


@user_passes_test(official_check)
@csrf_exempt
def attendance_workers(request):
    user = request.user
    user_details = Officials.objects.get(email_id = user.email)
    block_details = user_details.blocks
    workers = Workers.objects.filter(block=block_details)

    if request.method == 'POST':
        if request.POST.get('submit'):
            print('taking attendance')
            date=request.POST["datefield"]
            attendance_list=list()
            for stud in workers:
                attendance_list.append(request.POST[str(stud.staff_id)]) # Storing attendance for verification
                if (request.POST[str(stud.staff_id)] == 'Present'):
                    current = stud.attendance
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
                    current = stud.attendance
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
            for stud in workers:
                pos = stud.attendance.dates.find(get_date)
                if pos != -1:
                    if stud.attendance.dates[pos-1] == 'X':
                        stud.att = 'Absent'
                    else:
                        stud.att = 'Present'
            return render(request, 'officials/attendance-workers.html', {'off_details':user_details, 'block_details':block_details, 'stud_list':workers, 'get_date':get_date})
              

    return render(request, 'officials/attendance-workers.html', {'off_details':user_details, 'block_details':block_details, 'stud_list':workers, 'attendance': attendance})

@user_passes_test(official_check)
def attendance_log(request):
    user = request.user
    official = user.official

    return render(request, 'officials/attendance-log.html', {'off_details':official})

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
            if user_details.designation == 'Deputy Chief-Warden' or user_details.designation == 'Chief-Warden':
                return render(request, 'officials/attendance-log-chief.html', {'off_details':user_details, 'block_details':block_details, 'pres_stud':pres_stud, 'abse_stud':abse_stud})
            else:
                return render(request, 'officials/attendance-log.html', {'off_details':user_details, 'block_details':block_details, 'pres_stud':pres_stud, 'abse_stud':abse_stud})


        elif(request.POST["regno"]):
            regno = request.POST["regno"]
            if not Institutestd.objects.filter(regd_no=str(regno)).exists():
                messages.error(request, 'Invalid Student Roll No.')
                return redirect('officials:attendance_log')
            current = attendance.objects.get(regd_no_id=regno).dates
            dates = current.split(',')
            abse = list(filter(lambda x: (x.startswith('X')), dates))
            pres = list(filter(lambda x: not (x.startswith('X')), dates))
            abse = list(map(lambda x: x.replace('X',''), abse))

            if user_details.designation == 'Deputy Chief-Warden' or user_details.designation == 'Chief-Warden':
                return render(request, 'officials/attendance-log-chief.html', {'off_details':user_details, 'block_details':block_details, 'pres_dates':pres, 'abse_dates':abse})
            else:
                return render(request, 'officials/attendance-log.html', {'off_details':user_details, 'block_details':block_details, 'pres_dates':pres, 'abse_dates':abse})

            


@user_passes_test(official_check)
def grantOuting(request):
    user = request.user
    user_details = Officials.objects.get(email_id = user.email)
    block_details = user_details.blocks
    students = details.objects.filter(block_id=block_details)

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

    return render(request, 'officials/outingPending.html', {'off_details':user_details, 'stud_list':stud_list})


# @user_passes_test(chief_warden_check)
# @csrf_exempt
# def search(request):
#     user = request.user
#     user_details = Officials.objects.get(email_id = user.email)
#     send_blocks = Blocks.objects.all()
#     if request.method == 'POST':
#         if request.POST.get('regno'):
#             try:
#                 stud = Institutestd.objects.get(regd_no=str(request.POST.get('regno')))
#             except Institutestd.DoesNotExist:
#                 messages.error(request, 'Student with registration no. does not exist!')
#                 return redirect('officials:search')
#             block_details = details.objects.get(regd_no=stud)
#             block = Blocks.objects.get(block_id=block_details.block_id_id)
#             if attendance.objects.get(regd_no=stud).status=='':isPresent = 'Absent'
#             else: isPresent = attendance.objects.get(regd_no=stud).status
#             items={
#                 'stud':stud,
#                 'block_details':block_details,
#                 'block_name':block.block_name,
#                 'isPresent':isPresent
#             }
#             items_list = list()
#             items_list.append(items)

#             return render(request, 'officials/search.html', {'items_list':(items_list), 'send_blocks':send_blocks})

#         else:
#             block_name = Blocks.objects.get(block_id=request.POST['block']).block_name
            
#             studs = details.objects.filter(block_id=request.POST['block'])
#             items_list = list()
#             for stud in studs:
#                 info = Institutestd.objects.get(regd_no=str(stud.regd_no_id))
#                 block_details = details.objects.get(regd_no=info)
#                 if attendance.objects.get(regd_no=info).status=='':isPresent = 'Absent'
#                 else: isPresent = attendance.objects.get(regd_no=info).status
#                 items={
#                     'stud':info,
#                     'block_details':block_details,
#                     'block_name':block_name,
#                     'isPresent':isPresent
#                 }
#                 items_list.append(items)
#             return render(request, 'officials/search.html', {'items_list':(items_list), 'send_blocks':send_blocks})

#     return render(request, 'officials/search.html',{'send_blocks':send_blocks})

@user_passes_test(chief_warden_check)
@csrf_exempt
def blockSearch(request):
    user = request.user
    official = user.official
    blocks = Block.objects.all()

    if request.POST:
        block_id = request.GET.get('block')
        if request.POST.get('Add'):
            block = Block.objects.get(id = request.POST.get('block_id'))
            try:
                student = Student.objects.get(regd_no = request.POST.get('regd_no'))
                room_detail = student.roomdetail
                if room_detail.block:
                    messages.error(request, f'Student {student.regd_no} already alloted room in {room_detail.block.name} {room_detail.room()}!')
                else:
                    room_detail.block = block
                    room_detail.floor = request.POST.get('floor')
                    room_detail.room_no = request.POST.get('room_no')
                    room_detail.save()
                    messages.success(request, f'Student {student.regd_no} successfully alloted room in {room_detail.block.name} {room_detail.room()}!')
            except Student.DoesNotExist:
                messages.error(request, f'Student not found!')

        if request.POST.get('remove'):
            room_detail = RoomDetail.objects.get(id = request.POST.get('roomdetail_id'))
            room_detail.block = None
            room_detail.floor = None
            room_detail.room_no = None
            room_detail.save()
            messages.success(request, f'Student {room_detail.student.regd_no} removed from room.')

        return redirect(reverse_lazy('officials:blockSearch') + '?block={}'.format(block_id))

    if request.GET.get('block'):
        block = Block.objects.get(id=request.GET.get('block')) 
        return render(request, 'officials/block_layout.html',{'blocks':blocks, 'current_block': block})

    return render(request, 'officials/block_layout.html',{'blocks':blocks})
     
@user_passes_test(chief_warden_check)
def student_list(request):
    off_details = Officials.objects.get(email_id= request.user.email)
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

# @user_passes_test(chief_warden_check)
# def studentdelete (request):
#     students=Institutestd.objects.all()
#     if request.method=='POST':
#         print(request.POST)
#         for stud in students:
#             if request.POST.get("d"+str(stud.regd_no)):
#                 print(stud.regd_no)
#                 try:
#                     Institutestd.objects.get(regd_no=str(stud.regd_no)).delete()
#                     # User.objects.get(regd_no=str(stud.regd_no)).delete()
#                     attendance.objects.get(regd_no=str(stud.regd_no)).delete()
#                 except:
#                     pass
#                 messages.success(request,str(stud.regd_no)+" is deleted!")
#                 return redirect('officials:student_list')
#             elif request.POST.get("e"+str(stud.regd_no)):
#                 #response=redirect('officials:register_edit')
#                 #response.set_cookie('regd_no_edit',str(stud.regd_no))
#                 #return response
#                 std=Institutestd.objects.get(regd_no=str(stud.regd_no))
#                 return render(request,'officials/register.html',{'std':std})

@user_passes_test(chief_warden_check)
def emp_list(request):
    off_details = Officials.objects.get(email_id= request.user.email)
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

@user_passes_test(chief_warden_check)        
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
                    # credentials.objects.get(emp_id=str(stud.emp_id)).delete()
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


@user_passes_test(chief_warden_check)
def workers_list(request):
    off_details = Officials.objects.get(email_id= request.user.email)
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
                # try:
                    # credentials.objects.get(staff_id=str(stud.staff_id)).delete()
                    
                # except:
                #     pass
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


# @user_passes_test(chief_warden_check)
# @csrf_exempt
# def watercan(request):
#     name = request.COOKIES['username_off']
#     off_details = Officials.objects.get(emp_id=str(name))
#     block_details = Blocks.objects.get(emp_id_id=str(name))

#     if request.method == 'POST':
#         if request.POST.get('submit_btn'):
#             date = request.POST.get('date')
#             received = request.POST.get('received')
#             given = request.POST.get('given')

#             if WaterCan.objects.filter(block=block_details, date=date).exists():
#                 current = WaterCan.objects.get(block=block_details, date=date)
#                 current.received = received
#                 current.given = given
#                 current.save()
#             else:
#                 newCan = WaterCan(block=block_details, date=date, received=received, given=given)
#                 newCan.save()
#             messages.success(request, 'Water Cans Info updated')
#             return redirect('officials:watercan')

#         elif request.POST.get('count_btn'):
#             if request.POST.get('date_hist'):
#                 date_hist = request.POST.get('date_hist')
#                 if WaterCan.objects.filter(block=block_details, date=date_hist).exists():
#                     dateRec = WaterCan.objects.get(block=block_details, date=date_hist).received
#                     dateGiven = WaterCan.objects.get(block=block_details, date=date_hist).given
#                 else:
#                     dateRec = -10
#                     dateGiven = -10
#                 return render(request, 'officials/water-can.html', {'dateRec':dateRec, 'dateGiven':dateGiven, 'dateUsed':dateGiven})

#             elif request.POST.get('month_hist'):
#                 month = int(request.POST.get('month_hist').split('-')[1])
#                 if WaterCan.objects.filter(block=block_details, date__month=month).exists():
#                     month_set = WaterCan.objects.filter(block=block_details, date__month=month).order_by('-date')
#                     month_rec = month_set.aggregate(Sum('received'))['received__sum']
#                     month_given = month_set.aggregate(Sum('given'))['given__sum']
#                     month_used = month_given
#                     return render(request, 'officials/water-can.html', {'month':request.POST.get('month_hist'), 'month_empty':False, 'month_set':month_set, 'month_rec':month_rec, 'month_given':month_given, 'month_used':month_used})
#                 else:
#                     return render(request, 'officials/water-can.html', {'month_empty':True})



#     return render(request, 'officials/water-can.html')


from .forms import StudentForm
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

class OfficialTextMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_official

class ChiefWardenTestMixin(OfficialTextMixin):
    def test_func(self):
        is_official = super().test_func() 
        user = self.request.user
        if is_official:
            official = Officials.objects.get(email_id = user.email)
            is_chief = official.designation == 'Deputy Chief-Warden' or official.designation == 'Chief-Warden'

        return is_official and is_chief




class StudentRegisterView(CreateView):
    template_name = 'officials/student-register-form.html'
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('officials:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Student'
        return context

class StudentUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/student-register-form.html'
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('officials:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Student Details'
        return context

class StudentDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('officials:student_list')

class OfficialRegisterView(ChiefWardenTestMixin, CreateView):
    template_name = 'officials/official-register-form.html'
    model = Official
    fields = '__all__'
    success_url = reverse_lazy('officials:emp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Official'
        return context

class OfficialUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/official-register-form.html'
    model = Official
    fields = '__all__'
    success_url = reverse_lazy('officials:emp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Official Details'
        return context

class OfficialDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Official
    success_url = reverse_lazy('officials:emp_list')

class WorkerRegisterView(ChiefWardenTestMixin, CreateView):
    template_name = 'officials/official-register-form.html'
    model = Worker
    fields = '__all__'
    success_url = reverse_lazy('officials:workers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Staff'
        return context

class WorkerUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/official-register-form.html'
    model = Worker
    fields = '__all__'
    success_url = reverse_lazy('officials:workers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Staff Details'
        return context

class WorkerDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy('officials:workers_list')

