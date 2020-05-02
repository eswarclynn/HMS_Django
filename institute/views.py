from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.api import get_messages
from institute.models import Institutestd

# Create your views here.
def index(request):
    if request.COOKIES.get('username_std'):
        response = render(request, 'institute/index.html')
        response.delete_cookie('username_std')

    elif request.COOKIES.get('username_off'):
        response = render(request, 'institute/index.html')
        response.delete_cookie('username_off')

    else:
        response = render(request, 'institute/index.html')

    return response


