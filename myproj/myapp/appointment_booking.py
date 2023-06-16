# -*- coding: utf-8 -*-
"""
This module provides a functions  to book
appointments,check availability of
appointments and disable appointments

Created on Fri June 10 2023

Revised on Fri June 10 2023

created by A.piriyadharshini

"""
from bst import BST, serialize_bst, deserialize_bst
import json
import os
import csv
from datetime import datetime


def writejson(dictionary={}):
    """
    This function is used to
    write in json file
    args:dictionary
    """
    with open("appointments.json", "w") as outfile:
        json.dump(dictionary, outfile)


def readjson():
    """
    This function is used to read from
    json file
    """
    with open("appointments.json", "r") as f:
        data = json.load(f)
        return data


def timeslotgenerator(docterid, date, timeslot):
    """
    This function is used to generate time slots for
    a particular docter and day
    """
    dictionary = readjson()
    # if docterid is not available then a new dictionary is created
    if str(docterid) not in dictionary:
        binloc = BST()
        for i in timeslot:
            binloc.insert(i)
        temp = {}
        val = serialize_bst(binloc.root)
        temp[date] = val
        dictionary[docterid] = temp
        writejson(dictionary)
    # if docter id is already present then the values(dicitonary with date and timeslots for each day) are taken
    else:
        dates = dictionary.get(str(docterid))
        binloc = BST()
        for i in timeslot:
            binloc.insert(i)
        val = serialize_bst(binloc.root)
        dates[date] = val
        # print(dates)
        writejson(dictionary)


def checkavailability(docterid, date, time):
    """
    This function checks for availability of
    a timeslot
    """
    dictionary = readjson()
    # the dictionary containing dates are retrived
    dates = dictionary.get(str(docterid))
    # the serialised binary object correspodning to the date is obtained
    timeslot = dates.get(date)
    # the serialised bst is converted to deserialised
    val = deserialize_bst(timeslot)
    # then status of appointment is returned
    with open("Confirmedappointments.csv") as f:
        reader = csv.reader(f)
        flag = True
        for row in reader:
            if row[1] == str(docterid) and row[2] == date and row[3] == time:
                flag = False
                break
            flag = True
        a = val.find(time)
    return val.find(time) and flag


def bookappointment(patientid, docterid, date, time):
    """
    This function books appointment
    """
    if checkavailability(docterid, date, time):
        dictionary = readjson()
        dates = dictionary.get(str(docterid))
        timeslot = dates.get(date)
        val = deserialize_bst(timeslot)
        # the timeslot which is booked is removed from the binary search tree
        val.remove(time)
        # The bst is serialised and stored in json
        newval = serialize_bst(val.root)
        dates[date] = newval
        writejson(dictionary)

        with open("Confirmedappointments.csv", mode="a", newline="") as file:
            f = csv.writer(file)
            f.writerow(
                [
                    patientid,
                    docterid,
                    date,
                    time,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                ]
            )


if __name__ == "__main__":
    if not os.path.exists("Confirmedappointments.csv"):
        with open("Confirmedappointments.csv", mode="w", newline="") as file:
            pass
        file.close()
    if not os.path.exists("appointments.json"):
        writejson()
    # writejson()
    timeslot = [
        "09:00-09:30",
        "09:30-10:00",
        "10:00-10:30",
        "10:30-11:00",
        "11:00-11:30",
        "13:30-14:00",
        "14:00-14:30",
        "14:30-15:00",
        "15:00-15:30",
        "15:30-16:00",
        "16:00-16:30",
        "16:30-17:00",
    ]
    timeslotgenerator(1, "12-06-2023", timeslot)
    timeslot = [
        "09:00-09:30",
        "09:30-10:00",
        "10:00-10:30",
        "10:30-11:00",
        "11:00-11:30",
        # "13:30-14:00",
        # "14:00-14:30",
        "14:30-15:00",
        "15:00-15:30",
        "15:30-16:00",
        "16:00-16:30",
        "16:30-17:00",
    ]
    timeslotgenerator(2, "12-06-2023", timeslot)
    timeslot = [  # "09:00-09:30",
        #             "09:30-10:00",
        #             "10:00-10:30",
        #             "10:30-11:00",
        #             "11:00-11:30",
        "13:30-14:00",
        "14:00-14:30",
        "14:30-15:00",
        "15:00-15:30",
        "15:30-16:00",
        "16:00-16:30",
        "16:30-17:00",
    ]
    timeslotgenerator(1, "13-06-2023", timeslot)
    timeslot = [
        "09:00-09:30",
        "09:30-10:00",
        "10:00-10:30",
        "10:30-11:00",
        "11:00-11:30",
    ]
    # # "13:30-14:00",
    # # "14:00-14:30",
    # "14:30-15:00",
    # "15:00-15:30",
    # "15:30-16:00",
    # "16:00-16:30",
    # "16:30-17:00"]
    timeslotgenerator(2, "13-06-2023", timeslot)
    patientid = int(input("enter the userid:"))
    docterid = int(input("enter the docterid:"))
    date = input("enter the date:")
    d = {  #'12:00-12:30': checkavailability(docterid, date, '12:00-12:30'),
        #      '12:30-13:00': checkavailability(docterid, date, '12:30-13:00'),
        #      '13:00-13:30': checkavailability(docterid, date, '13:00-13:30'),
        "13:30-14:00": checkavailability(docterid, date, "13:30-14:00"),
        "14:00-14:30": checkavailability(docterid, date, "14:00-14:30"),
        "14:30-15:00": checkavailability(docterid, date, "14:30-15:00"),
        "15:00-15:30": checkavailability(docterid, date, "15:00-15:30"),
        "15:30-16:00": checkavailability(docterid, date, "15:30-16:00"),
        "16:00-16:30": checkavailability(docterid, date, "16:00-16:30"),
        "16:30-17:00": checkavailability(docterid, date, "16:30-17:00"),
        #  '17:00-17:30': checkavailability(docterid, date, '17:00-17:30'),
        #  '17:30-18:00': checkavailability(docterid, date, '17:30-18:00'),
        #  '18:00-18:30': checkavailability(docterid, date, '18:00-18:30'),
        #  '18:30-19:00': checkavailability(docterid, date, '18:30-19:00'),
        #  '19:00-19:30': checkavailability(docterid, date, '19:00-19:30'),
        #  '19:30-20:00': checkavailability(docterid, date,'19:30-20:00'),
        #  '20:00-20:30': checkavailability(docterid, date,'20:00-20:30'),
        #  '20:30-21:00': checkavailability(docterid, date, '20:30-21:00'),
        #  '21:00-21:30': checkavailability(docterid, date, '21:00-21:30'),
        #  '21:30-22:00': checkavailability(docterid, date, '21:30-22:00'),
        #  '22:00-22:30': checkavailability(docterid, date, '22:00-22:30'),
        #  '22:30-23:00': checkavailability(docterid, date, '22:30-23:00'),
        #  '23:00-23:30': checkavailability(docterid, date,  '23:00-23:30'),
        #  '23:30-24:00':checkavailability(docterid, date, '23:30-24:00'),
        #  '01:00-01:30': checkavailability(docterid, date, '01:00-01:30'),
        #  '01:30-02:00':checkavailability(docterid, date, '01:30-02:00'),
        #  '02:00-02:30': checkavailability(docterid, date,  '02:00-02:30'),
        #  '02:30-03:00': checkavailability(docterid, date, '02:30-03:00'),
        #  '03:00-03:30': checkavailability(docterid, date, '03:00-03:30'),
        #  '03:30-04:00': checkavailability(docterid, date, '03:30-04:00'),
        #  '04:00-04:30': checkavailability(docterid, date, '04:00-04:30'),
        #  '04:30-05:00': checkavailability(docterid, date, '04:30-05:00'),
        #  '05:00-05:30': checkavailability(docterid, date, '05:00-05:30'),
        #  '05:30-06:00': checkavailability(docterid, date, '05:30-06:00'),
        #  '06:00-06:30': checkavailability(docterid, date, '06:00-06:30'),
        #  '06:30-07:00': checkavailability(docterid, date, '06:30-07:00'),
        #  '07:00-07:30': checkavailability(docterid, date, '07:00-07:30'),
        #  '07:30-08:00': checkavailability(docterid, date, '07:30-08:00'),
        #  '08:00-08:30': checkavailability(docterid, date, '08:00-08:30'),
        #  '08:30-09:00': checkavailability(docterid, date, '08:30-09:00'),
        "09:00-09:30": checkavailability(docterid, date, "09:00-09:30"),
        "09:30-10:00": checkavailability(docterid, date, "09:30-10:00"),
        "10:00-10:30": checkavailability(docterid, date, "10:00-10:30"),
        "10:30-11:00": checkavailability(docterid, date, "10:30-11:00"),
        "11:00-11:30": checkavailability(docterid, date, "11:00-11:30"),
        #  '11:30-12:00': checkavailability(docterid, date,'11:30-12:00'),
    }

    for key, value in d.items():
        print(key, ":", value)

    timeslot = input("enter the time slot:")

    if checkavailability(docterid, date, timeslot) == True:
        bookappointment(patientid, docterid, date, timeslot)
    else:
        raise ValueError("Appointment not available")
