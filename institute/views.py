from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.messages.api import get_messages
from institute.models import Block, Student, Official

# Create your views here.
def index(request):
    return render(request, 'institute/index.html')

def gallery(request):
    return render(request, 'institute/grid-gallery.html')

def hostels(request):
    blocks = Block.objects.all()
    return render (request,'institute/hostels.html',{'blocks': blocks})

def contact(request):
    return render (request,'institute/contact.html')

def developers(request):
    return render(request,'institute/developers.html')