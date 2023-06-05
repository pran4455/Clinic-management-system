from django.shortcuts import render
# from django.http import HttpResponse
import csv
import datetime
import smtplib
import os
from email.message import EmailMessage
import random
# import time
# from django.contrib import messages

RANDOM_OTP = 0
RESET_EMAIL = ''

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

                        return render(request, 'homepage.html')  # Redirect to success page after successful login
                        # return render(request, 'patient_appointments.html') # change to required html file
                    else:
                        return render(request, 'index.html', {'alertmessage': 'Wrong password'})  # Display wrong password message

            return render(request, 'index.html', {'alertmessage': 'Username not found'})  # Display username not found message

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
            return render(request, 'register.html', {'alertmessage': 'Passwords do not match.'})

        with open('register.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
                print(email, row[3])
                if email == row[3]:
                    return render(request, 'register.html', {'alertmessage': 'E-mail already exists.'})

        with open('register.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, mobile, dob, email, password, address, age, gender, blood_group])

        return render(request, 'index.html', {'alertmessage': 'New user registration information stored successfully.'})

    return render(request, 'register.html')

def get_email(request):
    if request.method == "POST":
        email = request.POST['email']
        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            if email not in [row[3] for row in reader]:
                return render(request, 'forgot_password.html', {'message':'Email not found!'})
            else:
                global RANDOM_OTP, RESET_EMAIL
                RESET_EMAIL = email
                user = os.getenv('EMAIL_USER')
                key = 'rrsfsilblgzbiaep' # use os.getenv
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
                return render(request, 'validate_otp.html')
    return render(request, 'forgot_password.html')

def validate_otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        if password != confirm_password:
            return render(request, "validate_otp.html", {"alertmessage": "Passwords do not match!"})
        elif int(otp) != RANDOM_OTP:
            return render(request, "validate_otp.html", {"alertmessage": "Incorrect OTP!"})
        else:
            with open("register.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                global RESET_EMAIL
                for idx, row in enumerate(rows):
                    if row[3] == RESET_EMAIL:
                        RESET_EMAIL = ""
                        rows[idx][4] = password
                        break
            csvfile.close()
            with open("register.csv", "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            csvfile.close()
            return render(request, "index.html", {"alertmessage":"Reset Password Successful!"})
    else:
        return render(request, "validate_otp.html")








def testing(request):
    return render(request, "enter_prescription.html")


