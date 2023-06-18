from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path('/', views.home, name="home"),
    path("testing/", views.testing, name="testing"),
    path("register/", views.newregister, name="newregister"),
    path("login/", views.login, name="login"),
    path("forgot-password/", views.get_email, name="get_email"),
    path("validate-otp/", views.validate_otp, name="validate_otp"),
    path("personal-details/", views.personal_details, name="personal_details"),
    path("admin/", views.admin_home, name="admin_home"),
    path("patient/", views.patient_home, name="patient_home"),
    path("receptionist/", views.receptionist_home, name="receptionist_home"),
    path("doctor/", views.doctor_home, name="doctor_home"),
    path(
        "receptionist/receptionist-search-patient/",
        views.receptionist_search_patient,
        name="receptionist_search_patient",
    ),
    path(
        "doctor/doctor-search-patient/",
        views.doctor_search_patient,
        name="doctor_search_patient",
    ),
    path(
        "doctor/add-patient-details/",
        views.add_patient_details,
        name="add_patient_details",
    ),
    path(
        "doctor/doctor-prescription-search-patient/",
        views.doctor_prescription_search_patient,
        name="doctor_prescription_search_patient",
    ),
    path(
        "doctor/add-prescription-details/",
        views.add_prescription_details,
        name="add_prescription_details",
    ),
    path(
        "doctor/appointment-history/",
        views.doctor_appointment_history,
        name="doctor_appointment_history",
    ),
    path(
        "admin/view-registered-patients/",
        views.display_registered_patients,
        name="display_registered_patients",
    ),
    path(
        "admin/view-registered-receptionists/",
        views.display_registered_receptionists,
        name="display_registered_receptionists",
    ),
    path(
        "admin/view-registered-doctors/",
        views.display_registered_doctors,
        name="display_registered_doctors",
    ),
    path(
        "receptionist/appointment-homepage/",
        views.receptionist_appointment_homepage,
        name="receptionist_appointment_homepage",
    ),
    path(
        "receptionist/view-appointments/",
        views.receptionist_view_appointments,
        name="receptionist_view_appointments",
    ),
    path(
        "receptionist/appointment-search-patient/",
        views.receptionist_book_appointment,
        name="receptionist_book_appointment",
    ),
    path(
        "receptionist/appointment-history/",
        views.receptionist_view_appointments,
        name="receptionist_view_appointments",
    ),
    path(
        "receptionist/book-appointment/",
        views.book_local_appointment,
        name="book_local_appointment",
    ),
    path(
        "receptionist/view-local-appointments/",
        views.receptionist_view_local_appointments,
        name="receptionist_view_local_appointments",
    ),
    path(
        "receptionist/transaction-search-patient/",
        views.receptionist_transaction_search_patient,
        name="receptionist_transaction_search_patient",
    ),
    path("receptionist/payment-form/", views.payment_form, name="payment_form"),
    path(
        "patient/book-appointment/",
        views.patient_book_appointment,
        name="patient_book_appointment",
    ),
    path(
        "patient/appointment-history/",
        views.patient_appointment_history,
        name="patient_appointment_history",
    ),
    path(
        "patient/appointment-homepage/",
        views.patient_appointment_homepage,
        name="patient_appointment_homepage",
    ),
    path("patient/view-timeslots/", views.view_timeslots, name="view_timeslots"),
    path(
        "patient/view-history/", views.patient_view_history, name="patient_view_history"
    ),
    path(
        "patient/view-payments/",
        views.patient_view_payments,
        name="patient_view_payments",
    ),
    path(
        "receptionist/view-payments/",
        views.receptionist_view_payments,
        name="receptionist_view_payments",
    ),
    path(
        "receptionist/time-slot/",
        views.receptionist_time_slot,
        name="receptionist_time_slot",
    ),
    path("admin/register-doctor/", views.doctor_register, name="doctor_register"),
    path(
        "admin/register-receptionist/",
        views.receptionist_register,
        name="receptionist_register",
    ),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    # path('validate-otp/', lambda request: redirect('/clinic/forgot-password/'), name="validate_otp")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# check treatment, treatment advice, charges
