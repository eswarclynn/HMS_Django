from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from institute.models import Block, Student, Official
from students.models import Attendance, RoomDetail, Outing
from django.contrib import messages
from datetime import date as datePy
from django.http.response import Http404
from complaints.models import Complaint
from workers.models import Worker, Attendance as AttendanceWorker
from django.db.models import QuerySet
from django.db.models import Sum
import re

def official_check(user):
    return user.is_authenticated and user.is_official

def chief_warden_check(user):
    return official_check(user) and user.official.is_chief()


# Create your views here.
@user_passes_test(official_check)
def home(request):
    user = request.user
    official = user.official
    if official.is_chief():
        present_students = Attendance.objects.filter(status='Present')
        absent_students = Attendance.objects.filter(status='Absent')
        complaints = Complaint.objects.filter(status='Registered') | Complaint.objects.filter(status='Processing')

    else:
        if not official.block: 
            raise Http404('You are currently not appointed any block! Please contact Admin')

        student_rooms = official.block.roomdetail_set.all()
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
def attendance(request):
    user = request.user
    official = user.official
    block = official.block
    attendance_list  = Attendance.objects.filter(student__in=block.roomdetail_set.all().values_list('student', flat=True))
    date = None

    if request.method == 'POST' and request.POST.get('submit'):
        date = request.POST.get('date')
        for attendance in attendance_list:
            attendance.mark_attendance(date, request.POST.get(str(attendance.id)))

        messages.success(request, f'Attendance marked for date: {date}')

    if request.GET.get('for_date'):
        date = request.GET.get('for_date')
        messages.info(request, f'Selected date: {date}')
        for item in attendance_list:
            if item.present_dates and date in set(item.present_dates.split(',')): item.present_on_date = True
            if item.absent_dates and date in set(item.absent_dates.split(',')): item.absent_on_date = True

    return render(request, 'officials/attendance.html', {'official': official, 'attendance_list': attendance_list, 'date': date})


@user_passes_test(official_check)
@csrf_exempt
def attendance_workers(request):
    user = request.user
    official = user.official
    block = official.block
    attendance_list  = AttendanceWorker.objects.filter(worker__in=block.worker_set.all())
    date = None 

    if request.method == 'POST' and request.POST.get('submit'):
        date = request.POST.get('date')
        for attendance in attendance_list:
            attendance.mark_attendance(date, request.POST.get(str(attendance.id)))

        messages.success(request, f'Staff Attendance marked for date: {date}')

    if request.GET.get('for_date'):
        date = request.GET.get('for_date')
        messages.info(request, f'Selected date: {date}')
        for item in attendance_list:
            if item.present_dates and  date in set(item.present_dates.split(',')): item.present_on_date = True
            if item.absent_dates and date in set(item.absent_dates.split(',')): item.absent_on_date = True

    return render(request, 'officials/attendance_workers.html', {'official': official, 'attendance_list': attendance_list, 'date': date})


@user_passes_test(official_check)
def attendance_log(request):
    user = request.user
    official = user.official
    student = None
    present_attendance = None
    absent_attendance = None
    present_dates = None
    absent_dates = None

    if official.is_chief():
        attendance_list = Attendance.objects.all()
    else:
        attendance_list = Attendance.objects.filter(student__in = official.block.roomdetail_set.all().values_list('student', flat=True))

    if request.GET.get('by_regd_no'):
        student = attendance_list.get(student__regd_no = request.GET.get('by_regd_no')).student
        if student.attendance.present_dates: present_dates = student.attendance.present_dates.split(',') 
        if student.attendance.absent_dates: absent_dates = student.attendance.absent_dates.split(',')

    if request.GET.get('by_date'):
        present_attendance = attendance_list.filter(present_dates__contains = request.GET.get('by_date'))
        absent_attendance = attendance_list.filter(absent_dates__contains = request.GET.get('by_date'))

    return render(request, 'officials/attendance_log.html', {'official':official, 'student': student, 'date': request.GET.get('by_date'),'present_attendance': present_attendance, 'absent_attendance': absent_attendance, 'present_dates': present_dates, 'absent_dates': absent_dates})


@user_passes_test(official_check)
def generate_attendance_sheet(request):
    from .utils import AttendanceBookGenerator
    from django.utils import timezone
    from django.http import HttpResponse
    
    year_month = request.GET.get("year_month")
    block_id = request.GET.get("block_id")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename=Attendance({date}).xlsx'.format(date=timezone.now().strftime('%d-%m-%Y'),)
    
    BookGenerator = AttendanceBookGenerator(block_id, year_month)
    workbook = BookGenerator.generate_workbook()
    workbook.save(response)

    return response

@user_passes_test(official_check)
def grant_outing(request):
    user = request.user
    official = user.official
    outings = Outing.objects.filter(student__in=official.block.roomdetail_set.all().values_list('student', flat=True), permission="Pending")

    return render(request, 'officials/grant_outing.html', {'official': official, 'outings': outings})


@user_passes_test(official_check)
def outing_detail(request, pk):
    outing = get_object_or_404(Outing, id=pk)

    if request.POST.get('permission'):
        outing.permission = request.POST.get('permission')
        outing.save()

        messages.success(request, f'Outing successfully {outing.permission.lower()} to {outing.student.name}')
        return redirect('officials:grant_outing')
    return render(request, 'officials/outing_show.html', {'outing': outing})


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
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

class OfficialTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_official

class ChiefWardenTestMixin(OfficialTestMixin):
    def test_func(self):
        is_official = super().test_func() 
        return is_official and self.request.user.official.is_chief()

class StudentListView(OfficialTestMixin, ListView):
    model = Student
    template_name = 'officials/student_list.html'

    def get_queryset(self):
        if self.request.user.official.is_chief(): return Student.objects.all()
        else: return Student.objects.filter(roomdetail__block=self.request.user.official.block) 

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

class OfficialListView(ChiefWardenTestMixin, ListView):
    model = Official
    template_name = 'officials/official_list.html'

class OfficialRegisterView(ChiefWardenTestMixin, CreateView):
    template_name = 'officials/official-register-form.html'
    model = Official
    fields = ['emp_id', 'name', 'designation', 'phone', 'account_email', 'email']
    success_url = reverse_lazy('officials:emp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Official'
        return context

class OfficialUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/official-register-form.html'
    model = Official
    fields = ['emp_id', 'name', 'designation', 'phone', 'account_email', 'email']
    success_url = reverse_lazy('officials:emp_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Official Details'
        return context

class OfficialDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Official
    success_url = reverse_lazy('officials:emp_list')

class WorkerListView(ChiefWardenTestMixin, ListView):
    model = Worker
    template_name = 'officials/workers_list.html'

class WorkerRegisterView(ChiefWardenTestMixin, CreateView):
    template_name = 'officials/official-register-form.html'
    model = Worker
    fields = ['staff_id', 'name', 'designation', 'account_email', 'email', 'phone', 'gender', 'block']
    success_url = reverse_lazy('officials:workers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Staff'
        return context

class WorkerUpdateView(ChiefWardenTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'officials/official-register-form.html'
    model = Worker
    fields = ['staff_id', 'name', 'designation', 'account_email', 'email', 'phone', 'gender', 'block']
    success_url = reverse_lazy('officials:workers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Staff Details'
        return context

class WorkerDeleteView(ChiefWardenTestMixin, LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy('officials:workers_list')

