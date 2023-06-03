from django.shortcuts import render
from django.http import HttpResponse
import csv
import datetime
import smtplib
import os
from email.message import EmailMessage
import random

RANDOM_OTP = 0

def home(request):
    return render(request, 'index.html')


def new_page_view(request):
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Read the register.csv file
        with open('register.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                stored_username = row[3]
                stored_password = row[4]

                if username == stored_username:
                    if password == stored_password:
                        with open('logs.csv', 'a') as logs:
                            write = csv.writer(logs)
                            date_time = datetime.datetime.now()

                            current_time = date_time.time()
                            current_date = date_time.date()

                            write.writerow([current_date, current_time])

                        # return render(request, 'homepage.html')  # Redirect to success page after successful login
                        return render(request, 'patient_homepage.html')
                    else:
                        return render(request, 'index.html', {'message': 'Wrong password'})  # Display wrong password message

            return render(request, 'index.html', {'message': 'Username not found'})  # Display username not found message
    
    return render(request, 'index.html')


def newregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        address = request.POST['address']
        age = request.POST['age']
        gender = request.POST['gender']
        blood_group = request.POST['blood-group']

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match.'})
        
        with open('register.csv', 'a+') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if email == row[3]:
                    return render(request, 'register.html', {'error_message': 'E-mail already exists.'})

        with open('register.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, mobile, dob, email, password, address, age, gender, blood_group])

        return render(request, 'register.html', {'message': 'New user registration information stored successfully.'})
    
    return render(request, 'register.html')

'''

# send otp code:

if request.method == 'POST':
    global RANDOM_OTP
    email = request.POST['email']
    user = os.getenv('EMAIL_USER')
    key = 'rrsfsilblgzbiaep'
    RANDOM_OTP = random.randint(100000, 999999)
    msg = EmailMessage()
    msg["Subject"] = "OTP Verification for Resetting your Password"
    msg["From"] = user
    msg["To"] = email
    msg.set_content(
        """Hello """
        + str("User")
        + """,
                        This mail is in response to your request of resetting your clinic account password.

                    Please enter or provide the following OTP: """
        + str(RANDOM_OTP)
        + """

                    Note that this OTP is valid only for this instance. Requesting another OTP will make this OTP invalid. Incase you haven't requested to reset your password, contact your xyz. Thank You"""
    )
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(user, key)
    server.send_message(msg)
    server.quit()


'''


