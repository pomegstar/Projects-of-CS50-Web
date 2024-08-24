import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from hospitals.models import Doctor, Hospital
from accounts.models import Patient, User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def get_weekday_indices(weekday_str):
    weekday_map = {
        "sun": 6,
        "mon": 0,
        "tue": 1,
        "wed": 2,
        "thu": 3,
        "fri": 4,
        "sat": 5
    }
    weekdays = weekday_str.split(", ")
    return {day: weekday_map[day.lower()] for day in weekdays if day.lower() in weekday_map}


@login_required
def book(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        dat = request.POST['treatment_date']
        patient = Patient.objects.get(user=request.user)
        doctor = Doctor.objects.get(id=request.POST['doctor'])
        allowed_days = get_weekday_indices(doctor.weeks)
        age = request.POST['age']
        pro = request.POST['problem']
        treatment_date = datetime.strptime(dat, '%Y-%m-%d')
        if treatment_date <= datetime.today():
            return render(request, 'appointments/book.html', {
                "doctors": doctors,
                "message": "Invalid date. The treatment date cannot be in the past.",
            })
        if treatment_date.weekday() not in allowed_days.values():
            return render(request, 'appointments/book.html', {
                "doctors": doctors,
                "message": "Invalid date. Please choose a valid treatment date.",
            })
        if int(age) < 0:
            return render(request, 'appointments/book.html', {
                "doctors": doctors,
                "message": "Invalid age.",
            })
        serial_number = Appointment.objects.filter(
            doctor=doctor, treatment_date=dat, is_complete=False).count() + 1
        notBook = Appointment.objects.filter(
            doctor=doctor, patient=patient, treatment_date=dat).count() == 0
        if notBook:
            apnmnt = Appointment(
                patient=patient,
                doctor=doctor,
                treatment_date=dat,
                serial_number=serial_number,
                age=age,
                problem=pro,
            )
            apnmnt.save()
        else:
            return render(request, 'appointments/book.html', {
                "doctors": doctors,
                "message": "Already appointed on that day.",
            })

        return redirect('appointments:pndap')

    return render(request, 'appointments/book.html', {
        'doctors': doctors,
    })


@login_required
def appoint(request, id):
    dr = Doctor.objects.get(pk=id)
    pt = Patient.objects.get(user=request.user)
    allowed_days = get_weekday_indices(dr.weeks)
    apn = Appointment.objects.filter(doctor=dr, patient=pt)

    if request.method == 'POST':
        dat = request.POST['treatment_date']
        age = request.POST['age']
        pro = request.POST['problem']
        treatment_date = datetime.strptime(dat, '%Y-%m-%d')
        if treatment_date <= datetime.today():
            return render(request, 'appointments/appoint.html', {
                "did": id,
                "dr": dr,
                "message": "Invalid date. The treatment date cannot be in the past.",
                "apn": apn
            })
        if treatment_date.weekday() not in allowed_days.values():
            return render(request, 'appointments/appoint.html', {
                "did": id,
                "dr": dr,
                "message": "Invalid date. Please choose a valid treatment date.",
                "apn": apn
            })
        if int(age) < 0:
            return render(request, 'appointments/appoint.html', {
                "did": id,
                "dr": dr,
                "message": "Invalid age.",
                "apn": apn
            })
        serial_number = Appointment.objects.filter(
            doctor=dr, treatment_date=dat, is_complete=False).count() + 1
        notBook = Appointment.objects.filter(doctor=dr, patient=pt, treatment_date=dat).count() == 0
        if notBook:
            apnmnt = Appointment(
                patient=pt,
                doctor=dr,
                treatment_date=dat,
                serial_number=serial_number,
                age=age,
                problem=pro,
            )
            apnmnt.save()
        else:
            return render(request, 'appointments/appoint.html', {
                "did": id,
                "dr": dr,
                "message": "Already appointed on that day.",
                "apn": apn
            })
        apn = Appointment.objects.filter(doctor=dr, patient=pt)
        return render(request, 'appointments/appoint.html', {
            "did": id,
            "dr": dr,
            "mssage": "Appointment Successful!",
            "apn": apn
        })

    return render(request, 'appointments/appoint.html', {
        "did": id,
        "dr": dr,
        "apn": apn
    })


@login_required
@csrf_exempt
def patients(request):
    dr = Doctor.objects.get(user=request.user.id)
    pt = Appointment.objects.filter(is_complete=False, doctor=dr).order_by('treatment_date')
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get("date") is not None:
            dat = data["date"]
            ptd = Appointment.objects.filter(
                doctor=dr, is_complete=False, treatment_date=dat).order_by('serial_number')

            ptd_list = []
            for appointment in ptd:
                ptd_list.append({
                    'id': appointment.id,
                    'patient': appointment.patient.user.username,
                    'age': appointment.age,
                    'problem': appointment.problem,
                    'serial_number': appointment.serial_number,
                    'treatment_date': appointment.treatment_date
                })

            csrf_token = get_token(request)
            return JsonResponse({
                'fpatients': ptd_list,
                'csrf_token': csrf_token
            }, status=200)

    return render(request, 'appointments/patients.html', {
        "patients": pt
    })


def notify_patient(patient_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'appointments_{patient_id}',
        {
            'type': 'appointment_message',
            'message': message
        }
    )


@login_required
def del_ap(request, id):
    if request.method == 'POST':
        if request.POST.get('pat') == 'Patient':
            did = request.POST['dr_id']
            ap = Appointment.objects.get(pk=id)
            d_apns = Appointment.objects.filter(
                doctor=ap.doctor, treatment_date=ap.treatment_date, is_complete=False).order_by('serial_number')

            for apn in d_apns:
                if ap.serial_number < apn.serial_number:
                    apn.serial_number -= 1
                    apn.save()
                elif ap.serial_number >= apn.serial_number:
                    apn.serial_number = apn.serial_number
                    apn.save()
            ap.delete()

            for apn in d_apns:
                notify_patient(
                    apn.patient.user.id, f"Now your serial number is '{apn.serial_number}', doctor: {apn.doctor.user.username}, treatment date: {apn.treatment_date}. Refresh the page for reloading the new serial number.")

            if request.POST['my_all_ap'] == 'True':
                if request.POST['pending'] == 'True':
                    return redirect('appointments:pndap')
                else:
                    return redirect('appointments:allap')

            return redirect('appointments:appointment', id=did)

        elif request.POST.get('doc') == 'Doctor':
            ap = Appointment.objects.get(pk=id)
            d_apns = Appointment.objects.filter(
                doctor=ap.doctor, treatment_date=ap.treatment_date, is_complete=False).order_by('serial_number')

            for apn in d_apns:
                if ap.serial_number < apn.serial_number:
                    apn.serial_number -= 1
                    apn.save()
                elif ap.serial_number >= apn.serial_number:
                    apn.serial_number = apn.serial_number
                    apn.save()
            ap.is_complete = True
            ap.save()

            for apn in d_apns:
                notify_patient(
                    apn.patient.user.id, f"Now your serial number is '{apn.serial_number}', doctor: {apn.doctor.user.username}, treatment date: {apn.treatment_date}. Refresh the page for reloading the new serial number.")
            if request.POST['allpat'] == 'True':
                return redirect('appointments:allpat')
            else:
                return redirect('appointments:patients')

    elif request.method == 'PUT':
        ap = Appointment.objects.get(pk=id)
        d_apns = Appointment.objects.filter(
            doctor=ap.doctor, treatment_date=ap.treatment_date, is_complete=False).order_by('serial_number')

        for apn in d_apns:
            if ap.serial_number < apn.serial_number:
                apn.serial_number -= 1
                apn.save()
            elif ap.serial_number >= apn.serial_number:
                apn.serial_number = apn.serial_number
                apn.save()
        ap.is_complete = True
        ap.save()

        for apn in d_apns:
            notify_patient(
                apn.patient.user.id, f"Now your serial number is '{apn.serial_number}', doctor: {apn.doctor.user.username}, treatment date: {apn.treatment_date}. Refresh the page for reloading the new serial number.")

        ptd_list = []
        for appointment in d_apns:
            ptd_list.append({
                'id': appointment.id,
                'serial_number': appointment.serial_number
            })
        return JsonResponse({
            'serial': ptd_list,
        }, status=200)


@login_required
def allap(request):
    pt = Patient.objects.get(user=request.user.id)
    apn = Appointment.objects.filter(patient=pt).order_by('appointment_time').reverse()

    return render(request, 'appointments/myallap.html', {
        "appointments": apn
    })


@login_required
def pndap(request):
    pt = Patient.objects.get(user=request.user.id)
    apn = Appointment.objects.filter(
        patient=pt, is_complete=False).order_by('appointment_time').reverse()

    return render(request, 'appointments/myallap.html', {
        "appointments": apn,
        "pending": "Pending"
    })


@login_required
def allpat(request):
    dr = Doctor.objects.get(user=request.user.id)
    apn = Appointment.objects.filter(doctor=dr).order_by('appointment_time').reverse()

    return render(request, 'appointments/allpat.html', {
        "appointments": apn,
    })
