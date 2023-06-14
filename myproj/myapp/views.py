from django.shortcuts import render
from django.http import HttpResponse
import csv
import sys
import datetime
import smtplib
import os
from email.message import EmailMessage
import random

sys.path.append("D:/djangoProject/Clinic-management-system/myproj/myapp/")

import appointment_booking as apb

# import time
# from django.contrib import messages

RANDOM_OTP = 0
RESET_EMAIL = ''
CURRENT_USER = ''
CURRENT_PRIV = ''


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

                            write.writerow([username, current_date, current_time])

                            global CURRENT_USER, CURRENT_PRIV
                            CURRENT_USER = username

                        if row[-2] == "admin":
                            CURRENT_PRIV = "admin"
                            return render(request, "admin_homepage.html")
                        elif row[-2] == "rec":
                            CURRENT_PRIV = "rec"
                            return render(request, "homepage.html")
                        elif row[-2] == "pat":
                            CURRENT_PRIV = "pat"
                            return render(request, "patient_homepage.html")
                        elif row[-2] == "doc":
                            CURRENT_PRIV = "doc"
                            return render(request,
                                          "doctor_homepage.html")  # Redirect to success page after successful login
                    else:
                        return render(request, 'index.html',
                                      {'alertmessage': 'Wrong password'})  # Display wrong password message

            return render(request, 'index.html',
                          {'alertmessage': 'Username not found'})  # Display username not found message

    return render(request, 'index.html')


def newregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        address = request.POST['address'].replace(",", "-").replace("\r\n", ";")
        age = request.POST['age']
        gender = request.POST['gender']
        blood_group = request.POST['blood-group']

        if password != confirm_password:
            return render(request, 'register.html', {'alertmessage': 'Passwords do not match.'})

        with open('register.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if email == row[3]:
                    return render(request, 'register.html', {'alertmessage': 'E-mail already exists.'})

            uniqueid_random = str(random.randint(100000, 999999))
            while uniqueid_random in [row[-1] for row in reader]:
                uniqueid_random = str(random.randint(100000, 999999))

        with open('register.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [name, mobile, dob, email, password, address, age, gender, blood_group, "pat", uniqueid_random])

        with open('patients.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [name, mobile, dob, email, password, address, age, gender, blood_group, "pat", uniqueid_random])

        with open(f'./myapp/csv/{name}.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [name, mobile, dob, email, password, address, age, gender, blood_group, "pat", uniqueid_random, "None",
                 "None", "None"])

        return render(request, 'index.html', {'alertmessage': 'New user registration information stored successfully.'})

    return render(request, 'register.html')


def get_email(request):
    if request.method == "POST":
        email = request.POST['email']
        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            if email not in [row[3] for row in reader]:
                return render(request, 'forgot_password.html', {'message': 'Email not found!'})
            else:
                name = ""
                for row in reader:
                    if row[3] == email:
                        name = row[0]
                        break
                global RANDOM_OTP, RESET_EMAIL
                RESET_EMAIL = email
                user = os.getenv('EMAIL_USER')
                key = 'rrsfsilblgzbiaep'  # use os.getenv
                RANDOM_OTP = random.randint(100000, 999999)
                msg = EmailMessage()
                msg["Subject"] = "OTP Verification for Resetting your Password"
                msg["From"] = user
                msg["To"] = email
                msg.set_content(
                    """Hello """
                    + str(name)
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
            return render(request, "index.html", {"alertmessage": "Reset Password Successful!"})
    else:
        return render(request, "validate_otp.html")


def personal_details(request):
    with open("register.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == CURRENT_USER:
                priv = ""
                if row[-2] == "admin":
                    priv = "Administrator"
                    userhome = "admin"
                elif row[-2] == "rec":
                    priv = "Receptionist"
                    userhome = "receptionist"
                elif row[-2] == "pat":
                    priv = "Patient"
                    userhome = "patient"
                elif row[-2] == "doc":
                    priv = "Doctor"
                    userhome = "doctor"

                data = {
                    "uniqueid": row[-1],
                    "name": row[0],
                    "username": row[3],
                    "phone": row[1],
                    "gender": row[7],
                    "bloodgroup": row[8],
                    "dob": row[2],
                    "address": row[5].replace("-", ",").replace(";", "\\n"),
                    "age": row[6],
                    "priv": priv,
                    "userhome": userhome

                }
                return render(request, "personal_details.html", data)
        return render(request, "personal_details.html")


def admin_home(request):
    return render(request, "admin_homepage.html")


def patient_home(request):
    return render(request, "patient_homepage.html")


def receptionist_home(request):
    return render(request, "homepage.html")


def doctor_home(request):
    return render(request, "doctor_homepage.html")


def receptionist_search_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        current_name = ''
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "phone": row[1],
                        "gender": row[7],
                        "last_appointment": row[-3],
                        "address": row[5].replace("-", ",").replace(";", "\\n"),
                        "upcoming_appointment": row[-2],
                        "doctor_name": row[-1],
                        "blood_group": row[8]
                    }
                    break

            return render(request, "receptionist_view_patient_details.html", data)
        elif patient_name:
            current_name = patient_name
            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "phone": row[1],
                        "gender": row[7],
                        "last_appointment": row[-3],
                        "address": row[5].replace("-", ",").replace(";", "\\n"),
                        "upcoming_appointment": row[-2],
                        "doctor_name": row[-1],
                        "blood_group": row[8]
                    }
                    break

            return render(request, "receptionist_view_patient_details.html", data)
        else:
            return render(request, "receptionist_search_patient.html", {"alertmessage": "Patient not found!"})

    return render(request, "receptionist_search_patient.html")


def doctor_search_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        current_name = ''
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
                        break
                else:
                    return render(request, "doctor_search_patient.html", {"alertmessage": "Patient not found!"})
            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                basic_details = next(reader)
                uniqueid = basic_details[-4]
                name = basic_details[0]
                age = basic_details[6]
                sex = basic_details[7]
                phone = basic_details[1]
                address = basic_details[5].replace("-", ",").replace(";", "\\n")
                data = {
                    "uniqueid": uniqueid,
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "phone": phone,
                    "address": address,

                }

            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                if len([row for row in reader]) < 2:
                    data["alertmessage"] = "Patient details are not entered! Please enter them now!"
                    return render(request, "doctor_add_patient_details.html", data)

            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                details = next(reader)

                prescription = details[6].replace("-",",").replace(";", "\\n")
                dental_carries = details[7].replace("-", ",").replace(";", "\\n")
                missing_teeth = details[8].replace("-", ",").replace(";", "\\n")
                allergy = details[9].replace("-", ",").replace(";", "\\n")
                examination = details[10].replace("-", ",").replace(";", "\\n")
                abrasions = details[11].replace("-", ",").replace(";", "\\n")
                treatment_advice = details[12].replace("-", ",").replace(";", "\\n")
                treatment = details[13].replace("-", ",").replace(";", "\\n")
                treatment_charges = details[14].replace("-", ",").replace(";", "\\n")
                newdata = {
                    "prescription": prescription,
                    "dental_carries": dental_carries,
                    "missing_teeth": missing_teeth,
                    "allergy": allergy,
                    "examination": examination,
                    "abrasions": abrasions,
                    "treatment_advice": treatment_advice,
                    "treatment": treatment,
                    "treatment_charges": treatment_charges,
                }
                data.update(newdata)
                return render(request, "doctor_view_patient_details.html", data)


        elif patient_name:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0].strip() == patient_name.strip():
                        current_name = row[0]
                        break
                else:
                    return render(request, "doctor_search_patient.html", {"alertmessage": "Patient not found!"})
            current_name = patient_name
            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                basic_details = next(reader)
                uniqueid = basic_details[-4]
                name = basic_details[0]
                age = basic_details[6]
                sex = basic_details[7]
                phone = basic_details[1]
                address = basic_details[5].replace("-", ",").replace(";", "\\n")
                data = {
                    "uniqueid": uniqueid,
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "phone": phone,
                    "address": address,

                }

            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                if len([row for row in reader]) < 2:
                    data["alertmessage"] = "Patient details are not entered! Please enter them now!"
                    return render(request, "doctor_add_patient_details.html", data)

            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                details = next(reader)

                prescription = details[6].replace("-",",").replace(";", "\\n")
                dental_carries = details[7].replace("-", ",").replace(";", "\\n")
                missing_teeth = details[8].replace("-", ",").replace(";", "\\n")
                allergy = details[9].replace("-", ",").replace(";", "\\n")
                examination = details[10].replace("-", ",").replace(";", "\\n")
                abrasions = details[11].replace("-", ",").replace(";", "\\n")
                treatment_advice = details[12].replace("-", ",").replace(";", "\\n")
                treatment = details[13].replace("-", ",").replace(";", "\\n")
                treatment_charges = details[14].replace("-", ",").replace(";", "\\n")
                newdata = {
                    "prescription": prescription,
                    "dental_carries": dental_carries,
                    "missing_teeth": missing_teeth,
                    "allergy": allergy,
                    "examination": examination,
                    "abrasions": abrasions,
                    "treatment_advice": treatment_advice,
                    "treatment": treatment,
                    "treatment_charges": treatment_charges,
                }
                data.update(newdata)
                return render(request, "doctor_view_patient_details.html", data)

        else:
            return render(request, "doctor_search_patient.html", {"alertmessage": "Please fill any one field!"})

    return render(request, "doctor_search_patient.html")


def add_patient_details(request):
    if request.method == "POST":
        uniqueid = request.POST.get("unique-id")
        name = request.POST.get("full-name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        phone = request.POST.get("phone-number")
        address = request.POST.get("address")
        # prescription = request.POST.get("prescription").replace(",", "-").replace(",", "-").replace("\r\n", ";")
        dental_carries = request.POST.get("dental-carries").replace(",", "-").replace("\r\n", ";")
        missing_teeth = request.POST.get("missing-teeth").replace(",", "-").replace("\r\n", ";")
        allergy = request.POST.get("allergy").replace(",", "-").replace("\r\n", ";")
        abrasions = request.POST.get("abrasions").replace(",", "-").replace("\r\n", ";")
        with open(f"./myapp/csv/{name}.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([uniqueid, name, age, sex, phone, address, "None", dental_carries, missing_teeth, allergy, "None", abrasions, "None", "None", "None"])
        return render(request, "doctor_search_patient.html", {"alertmessage": "Details saved successfully!"})

    return render(request, "doctor_add_patient_details.html")

def doctor_prescription_search_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        current_name = ''
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
                        break
                else:
                    return render(request, "doctor_prescription_search_patient.html", {"alertmessage": "Patient not found!"})
            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                basic_details = next(reader)
                uniqueid = basic_details[-4]
                name = basic_details[0]
                age = basic_details[6]
                sex = basic_details[7]
                phone = basic_details[1]
                address = basic_details[5].replace("-", ",").replace(";", "\\n")
                data = {
                    "uniqueid": uniqueid,
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "phone": phone,
                    "address": address,
                }

            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                if len([row for row in reader]) < 2:
                    data["alertmessage"] = "Patient details are not entered! Please enter them now!"
                    return render(request, "doctor_add_patient_details.html", data)

            return render(request, "enter_prescription.html", data)

        elif patient_name:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0].strip() == patient_name.strip():
                        current_name = row[0]
                        break
                else:
                    return render(request, "doctor_search_patient.html", {"alertmessage": "Patient not found!"})
            current_name = patient_name
            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                basic_details = next(reader)
                uniqueid = basic_details[-4]
                name = basic_details[0]
                age = basic_details[6]
                sex = basic_details[7]
                phone = basic_details[1]
                address = basic_details[5].replace("-", ",").replace(";", "\\n")
                data = {
                    "uniqueid": uniqueid,
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "phone": phone,
                    "address": address,
                }

            with open(f"./myapp/csv/{current_name}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                if len([row for row in reader]) < 2:
                    data["alertmessage"] = "Patient details are not entered! Please enter them now!"
                    return render(request, "doctor_add_patient_details.html", data)

            return render(request, "enter_prescription.html", data)

        else:
            return render(request, "doctor_prescription_search_patient.html", {"alertmessage": "Please fill any one field!"})

    return render(request, "doctor_prescription_search_patient.html")

def add_prescription_details(request):
    if request.method == "POST":
        current_name = request.POST.get("name")
        medical_prescription = request.POST.get("prescription").replace(",", "-").replace("\r\n", ";")
        examination = request.POST.get("examination").replace(",", "-").replace("\r\n", ";")
        treatment = request.POST.get("treatment").replace(",", "-").replace("\r\n", ";")
        advice = request.POST.get("advice").replace(",", "-").replace("\r\n", ";")
        with open(f"./myapp/csv/{current_name}.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([examination, medical_prescription, treatment, advice])

        with open(f"./myapp/csv/{current_name}.csv", "r") as oldfile, open(f"./myapp/csv/{current_name}.tmp",
                                                                           "w", newline='') as newfile:
            reader = csv.reader(oldfile)
            writer = csv.writer(newfile, quoting=csv.QUOTE_NONE, escapechar='\\')

            myrow = [row for row in reader]


            myrow[1][6] = medical_prescription
            myrow[1][10] = examination
            myrow[1][12] = treatment
            myrow[1][13] = advice


            for row in myrow:
                writer.writerow(row)

        os.replace(f"./myapp/csv/{current_name}.tmp", f"./myapp/csv/{current_name}.csv")
        return render(request, "doctor_prescription_search_patient.html", {"alertmessage": "Prescription added successfully!"})
    return render(request, "enter_prescription.html")

def display_registered_patients(request):
    class Patient:
        def __init__(self, row):
            self.uniqueid =  row[10]
            self.name =  row[0]
            self.phonenumber =  row[1]
            self.dob =  row[2]
            self.email =  row[3]
            self.address =  row[5].replace("-", ",").replace(";", "\\n")
            self.age =  row[6]
            self.gender =  row[7]
            self.blood =  row[8]
            self.privilege =  "Patient" if row[9] == "pat" else ""

    with open("patients.csv") as csvfile:
        reader = csv.reader(csvfile)
        patient_data = []
        for i in reader:
            patient_data.append(Patient(i))
        data = {"patients": patient_data}
    return render(request, "display_registered_patients.html", data)


def receptionist_view_appointments(request):
    return render(request, "index.html")

def receptionist_appointment_homepage(request):
    return render(request, "receptionist_appointment_homepage.html")

def testing(request):
    return render(request, "edit_timeslots.html")

def receptionist_time_slot(request):
    if request.method == "POST":
        if not os.path.exists("Confirmedappointments.csv"):
            with open("Confirmedappointments.csv", mode='w', newline='') as file:
                pass
            file.close()
        if not os.path.exists("appointments.json"):
            apb.writejson()


        doctor = request.POST.get("doctor")
        doctorid = None
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == doctor:
                    doctorid = row[-1]
                    break

        olddate = request.POST.get("date").split("-")
        olddate.reverse()
        date = ""
        for d in olddate:
            date += d +"-"
        date = date[:-1]
        oldtimeslot = request.POST.getlist('slots')
        slot_dict = {
            "slot1": "09:00-09:30",
            "slot2": "09:30-10:00",
            "slot3": "10:00-10:30",
            "slot4": "10:30-11:00",
            "slot5": "11:00-11:30",
            "slot6": "13:30-14:00",
            "slot7": "14:00-14:30",
            "slot8": "14:30-15:00",
            "slot9": "15:00-15:30",
            "slot10": "15:30-16:00",
            "slot11": "16:00-16:30",
            "slot12": "16:30-17:00",
        }
        timeslot = []
        for t in oldtimeslot:
            timeslot.append(slot_dict.get(t))

        for time in timeslot:

            apb.timeslotgenerator(doctorid, date, timeslot)

        return render(request, "homepage.html", {"alertmessage": "Time slot edited successfully!"})
    else:
        class Doctor:
            def __init__(self, name):
                self.name = name
        doctors = []
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                doctors.append(Doctor(row[0]))
        data = {"doctors": doctors}
        return render(request, "edit_timeslots.html", data)

def receptionist_book_appointment(request):
    return render(request, "receptionist_book_appointment.html")

def patient_book_appointment(request):
    if request.method == "POST":
        date = request.POST.get("date")
        doctor = request.POST.get("doctor")
        pid = request.POST.get("uniqueid")
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == doctor:
                    d_uniqueid = row[-1]
                    data = {
                        "d_uniqueid" : d_uniqueid,
                        "p_uniqueid": pid,
                        "date": date
                    }
                    break
        return view_timeslots(request, data)
        # return render(request, "select_timeslot.html", data)
    class Doctor:
        def __init__(self, name):
            self.name = name
    doctors = []
    with open("doctors.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            doctors.append(Doctor(row[0]))
    data = {"doctors": doctors}

    with open("patients.csv") as csvfile:
        reader = csv.reader(csvfile)
        # print(CURRENT_USER)
        for row in reader:
            if row[3] == CURRENT_USER:
                temp = {
                    "name" : row[0],
                    "uniqueid" : row[-1],
                    "age" : row[6],
                    "sex": row[7],
                    "address": row[5].replace("-", ",").replace(";", "\\n"),
                }
                data.update(temp)
                break


    return render(request, "patient_book_appointment.html", data)

def view_timeslots(request, data):
    if not os.path.exists("Confirmedappointments.csv"):
        with open("Confirmedappointments.csv",mode='w', newline='') as file:
            pass
        file.close()
    if not os.path.exists("appointments.json"):
        apb.writejson()
    return render(request, "select_timeslot.html")
def logout(request):
    return render(request, "index.html")

