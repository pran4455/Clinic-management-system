from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def new_page_view(request):
    return render(request, 'register.html')

# Create your views here.
