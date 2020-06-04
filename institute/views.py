from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.api import get_messages
from institute.models import Blocks, Institutestd
from students.models import attendance, details

# Create your views here.
def index(request):
    if request.COOKIES.get('username_std'):
        response = render(request, 'institute/index.html')
        response.delete_cookie('username_std')

    elif request.COOKIES.get('username_off'):
        response = render(request, 'institute/index.html')
        response.delete_cookie('username_off')

    elif request.COOKIES.get('username_staff'):
        response = render(request, 'institute/index.html')
        response.delete_cookie('username_staff')

    else:
        response = render(request, 'institute/index.html')

    return response
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
