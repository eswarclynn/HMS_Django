from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from workers.models import Medical, Workers
from institute.models import Blocks, Institutestd, Officials
from complaints.models import Complaints, OfficialComplaints
from students.models import details
from django.contrib import messages

# Create your views here.
@csrf_exempt
def staff_home(request):
    staff_id = request.COOKIES['username_staff']
    user_details = Workers.objects.get(staff_id=str(staff_id))
    

    complaints = list()
    off_complaints = list()
    if user_details.designation == 'General Servant':
        studs = details.objects.filter(block_id=Blocks.objects.get(block_id=str(user_details.block.block_id)))
        for stud in studs:
            complaints += list((Complaints.objects.filter(regd_no=str(stud.regd_no), type='Room Cleaning', status='Registered')))
        off_complaints += list(OfficialComplaints.objects.filter(regd_no= Blocks.objects.get(block_id=str(user_details.block.block_id)).emp_id, type='Room Cleaning', status='Registered'))
        
    if user_details.designation == 'Scavenger':
        studs = details.objects.filter(block_id=Blocks.objects.get(block_id=str(user_details.block.block_id)))
        for stud in studs:
            complaints += list((Complaints.objects.filter(regd_no=str(stud.regd_no), type='Restroom Cleaning', status='Registered')))
        off_complaints += list(OfficialComplaints.objects.filter(regd_no= Blocks.objects.get(block_id=str(user_details.block.block_id)).emp_id, type='Restroom Cleaning', status='Registered'))

    if user_details.designation == 'Electrician':
            complaints += list((Complaints.objects.filter(type='Electrical', status='Registered')))
            off_complaints += list(OfficialComplaints.objects.filter(type='Electrical', status='Registered'))
    if user_details.designation == 'Mess Incharge':
            complaints += list((Complaints.objects.filter(type='Food Issues', status='Registered')))
            off_complaints += list(OfficialComplaints.objects.filter(type='Food Issues', status='Registered'))

    medical = list()
    if user_details.designation == 'Doctor':
        med_comp = Medical.objects.filter(status='Registered')
        for item in med_comp:
            try:
                room_det = details.objects.get(regd_no=item.regd_no)
                designation = 'Student'
                medical.append({
                    'comp':item,
                    'designation': designation,
                    'room':room_det.room_no,
                    'floor':room_det.floor[0],
                    'block': room_det.block_id.block_name,
                    'info': Institutestd.objects.get(regd_no=item.regd_no)
                })
                
            except Exception as e: 
                print(e)
                print('Not student')
            
            try:
                off_det = Officials.objects.get(emp_id=item.regd_no)
                designation = 'Staff'
                medical.append({
                    'comp':item,
                    'designation': designation,
                    'info': off_det
                })
            except: print('Not Official')
            try:
                work_det = Workers.objects.get(staff_id = item.regd_no)
                designation = 'Staff'
                medical.append({
                    'comp':item,
                    'designation': designation,
                    'info': work_det
                })
            except: print('Not Staff')
            print(medical)

        if request.method == 'POST':
            print(request.POST)
            for item in medical:
                newComplaint = Medical.objects.get(id=item['comp'].id)
                print(str(item['comp'].id))
                if newComplaint.status != request.POST[str(item['comp'].id)] and newComplaint.remarks != request.POST['RE'+str(item['comp'].id)]:
                    newComplaint.status = request.POST[str(item['comp'].id)]
                    newComplaint.remarks = request.POST['RE'+str(item['comp'].id)]
                    newComplaint.save()
            else:
                messages.success(request, 'Successfully updated Medical Issues!')
                return redirect('workers:staff_home') 
    if user_details.block: block_details = Blocks.objects.filter(block_id=user_details.block.block_id)
    else: block_details=""
    return render(request, 'workers/workers-profile.html', {'user_details': user_details, 'block_details':block_details, 'complaints':complaints,'off_complaints':off_complaints, 'medical':medical})


def medical_issue(request):
    if request.method == 'POST':
        if request.COOKIES.get('username_std'):
                newComplaint = Medical(
                regd_no = request.COOKIES['username_std'],
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )
        elif request.COOKIES.get('username_off'):
                newComplaint = Medical(
                regd_no = request.COOKIES['username_off'],
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )
        elif request.COOKIES.get('username_staff'):
                newComplaint = Medical(
                regd_no = request.COOKIES['username_staff'],
                summary = request.POST['summary'],
                detailed = request.POST['detailed'],
                )

        else:
            raise Http404('Please Log In and then register medical issue!')
                
        newComplaint.save()
        messages.success(request, 'Medical Issue Registered Successfully!')
        return redirect('workers:medical_issue')



    return render(request, 'workers/medical.html')