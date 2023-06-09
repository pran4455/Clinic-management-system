from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    # path('/', views.home, name="home"),
    path('testing/', views.testing, name='testing'),
    path('register/', views.newregister, name='newregister'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.get_email, name="get_email"),
    path('validate-otp/', views.validate_otp, name="validate_otp"),
    path('personal-details/', views.personal_details, name="personal_details"),
    path('admin/', views.admin_home, name="admin_home"),
    path('patient/', views.patient_home, name="patient_home"),
    path('receptionist/', views.receptionist_home, name="receptionist_home"),
    path('doctor/', views.doctor_home, name="doctor_home"),
    path('receptionist/receptionist-search-patient/', views.receptionist_search_patient, name="receptionist_search_patient"),
    path('doctor/doctor-search-patient/', views.doctor_search_patient, name="doctor_search_patient"),
    path('doctor/add-patient-details/', views.add_patient_details, name="add_patient_details"),
    path('doctor/doctor-prescription-search-patient/', views.doctor_prescription_search_patient, name="doctor_prescription_search_patient"),
    path('doctor/add-prescription-details/', views.add_prescription_details, name="add_prescription_details"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    # path('validate-otp/', lambda request: redirect('/clinic/forgot-password/'), name="validate_otp")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# check treatment, treatment advice, charges