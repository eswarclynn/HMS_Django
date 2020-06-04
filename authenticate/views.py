from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import credentials
from institute.models import Blocks, Institutestd, Officials
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from students.models import attendance, details
from django.core.mail import send_mail
from hosteldb.settings import EMAIL_HOST_USER
from workers.models import Workers
from workers.models import attendance as ATTWORK



# Create your views here.

def login(request):
    
    if request.method == 'POST':
        user = request.POST["username"]
        password1 = request.POST["password"]
        if credentials.objects.filter(regd_no=user, password=password1).exists():
            response = redirect('students:student_home')
            response.set_cookie('username_std',user)
            return response

        elif credentials.objects.filter(emp_id=user, password=password1).exists():
            response = redirect('officials:official_home')
            response.set_cookie('username_off',user)
            return response

        elif credentials.objects.filter(staff_id=user, password=password1).exists():
            response = redirect('workers:staff_home')
            response.set_cookie('username_staff',user)
            return response            

        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('authenticate:login')
            

    return render(request, 'authenticate/login.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        regno = request.POST["regno"]
        password1 = request.POST["pass"]
        mode = request.POST["type"]
    
        if(mode == 'student'):
            if credentials.objects.filter(regd_no=regno).exists():
                messages.error(request, 'Student already exists. Please Login!')
                return redirect('authenticate:signup')
            
            else:
                if Institutestd.objects.filter(regd_no = regno).exists():
                    newStudent = Institutestd.objects.get(regd_no = regno)

                    newCred = credentials(regd_no= Institutestd.objects.get(regd_no = regno), password=password1)
                    newCred.save()
                    addStudent = details(regd_no=newStudent)
                    addStudent.save()
                    addAttendance = attendance(regd_no=newStudent)
                    addAttendance.save()
                    messages.success(request, 'Student added to Hostels successfully')
                    return redirect('authenticate:signup')

                else:
                    messages.error(request, 'No student with given Registration no.')
                    return redirect('authenticate:signup')

        elif(mode == 'official'):
            if credentials.objects.filter(emp_id=regno).exists():
                messages.error(request, 'Official already exists. Please Login!')
                return redirect('authenticate:signup')
            
            else:
                if Officials.objects.filter(emp_id = regno).exists():
                    newCred = credentials(emp_id= Officials.objects.get(emp_id = regno), password=password1)
                    newCred.save()
                    messages.success(request, 'User added to hostels successfully!')
                    return redirect('authenticate:signup')
                else:
                    messages.error(request, 'No Official with given Registration no.')
                    return redirect('authenticate:signup')

        elif(mode == 'staff'):
            if credentials.objects.filter(staff_id=regno).exists():
                messages.error(request, 'Staff already exists. Please Login!')
                return redirect('authenticate:signup')
            
            else:
                if Workers.objects.filter(staff_id = regno).exists():
                    newCred = credentials(staff_id= Workers.objects.get(staff_id = regno), password=password1)
                    newCred.save()
                    addAttendance = ATTWORK(staff_id=Workers.objects.filter(staff_id = regno))
                    addAttendance.save()
                    messages.success(request, 'User added to hostels successfully!')
                    return redirect('authenticate:signup')
                else:
                    messages.error(request, 'No Staff with given Registration no.')
                    return redirect('authenticate:signup')                    
    
    
    return render(request, 'authenticate/SignUp1.html')



def forgot(request):
    if request.method == 'POST':
        user = request.POST["username"]
        if credentials.objects.filter(regd_no=user).exists():
            newPass = credentials.objects.get(regd_no_id=str(user))
            use=Institutestd.objects.get(regd_no=user)
            email=use.email_id
            subject="NIT AP Hostel Management System-Forgot Password request!"
            message="The password for the username \n"+str(user)+" is "+"\n Password : "+str(newPass.password)+"\nThis is a computer generated message dont reply to this !This is from Hostel Management System NIT AP .If it is not you please report to admin of the website "
            recepient=str(email)
            send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)
            messages.success(request, 'Password is sent to your mail id!')
            return redirect('authenticate:login')

        elif credentials.objects.filter(emp_id=user).exists():
            newPass = credentials.objects.get(emp_id_id=str(user))
            use=Officials.objects.get(emp_id=user)
            email=use.email_id
            subject="NIT AP Hostel Management System-Forgot Password request!"
            message="The password for the username \n"+str(user)+" is "+"\n Password : "+str(newPass.password)+"\nThis is a computer generated message dont reply to this !This is from Hostel Management System NIT AP .If it is not you please report to admin of the website "
            recepient=str(email)
            send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)
            messages.success(request, 'Password is sent to your mail id!')
            return redirect('authenticate:login')

        else:
            messages.error(request, 'Invalid Username')
            return redirect('authenticate:forgot')    

    return render(request, 'authenticate/forgot.html')