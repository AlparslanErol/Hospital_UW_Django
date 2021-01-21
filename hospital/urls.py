from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='hospital-home'),
    path('about/', views.about, name='hospital-about'),
    path('doctor/', views.doctor, name='hospital-doctor'),
    path('doctor/add/', views.add_doctor, name='hospital-doctor-add'),
    path('patient/', views.patient, name='hospital-patient'),
    path('patient/add/', views.add_patient, name='hospital-patient-add'),
    path('diagnosis/', views.diagnosis, name='hospital-diagnosis'),
    path('visitprocess/', views.visit, name='hospital-v-process'),
    path('visit/', views.visit, name='hospital-visit'),
    path('service/', views.service, name='hospital-service'),
    # path('etc/', views.about, name='hospital-etc'),
]