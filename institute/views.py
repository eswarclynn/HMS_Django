from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.api import get_messages
from institute.models import Blocks, Institutestd,Officials
from students.models import attendance, details

# Create your views here.
def index(request):
    return render(request, 'institute/index.html')

@csrf_exempt
def search(request):
    if request.method == 'POST':

        if request.POST.get('regno'):
            stud = Institutestd.objects.get(regd_no=str(request.POST.get('regno')))
            block_details = details.objects.get(regd_no=stud)
            block = Blocks.objects.get(block_id=block_details.block_id_id)
            items={
                'stud':stud,
                'block_details':block_details,
                'block_name':block.block_name,
            }
            print(items)
            return render(request,'institute/searchResult.html', {'user_details':items})

    return render(request,'institute/searchResult.html')

def gallery(request):
    return render(request, 'institute/grid-gallery.html')

def hostels(request):
    emp=Officials.objects.all()
    caretaker=list()

    for em in emp:

        try:
            if Blocks.objects.filter(emp_id=em).exists():
                block_name=Blocks.objects.get(emp_id=em).block_name
                caretaker.append({
                    'block':block_name,
                    'ph':em.phone,
                    'name':em.name,
                })
        except:
            pass
          
    return render (request,'institute/hostels.html',{'caretaker':caretaker,})

def contact(request):
    return render (request,'institute/contact.html')

def information(request):
    return render(request,'institute/information.html',{})