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

def newregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        dob = request.POST['name']
        email = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        address = request.POST['address']
        age = request.POST['age']
        gender = request.POST['gender']
        blood_group = request.POST['blood-group']

        with open('register.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, mobile, dob, email, password, confirm_password, address, age, gender, blood_group])

        return render(request, 'register.html', {'message': 'new user registeration information stored successfully.'})
    
    return render(request, 'register.html')

    

