from django.shortcuts import render
import csv

from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def new_page_view(request):
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        with open('logins.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password])

        return render(request, 'index.html', {'message': 'login information stored successfully.'})

    return render(request, 'index.html')


# Create your views here.
