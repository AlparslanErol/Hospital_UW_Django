from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='hospital-home'),
    path('about/', views.about, name='hospital-about'),
    path('doctor/', views.doctor, name='hospital-doctor'),
    path('doctor/add/', views.add_doctor, name='hospital-doctor-add'),
    path('doctor/delete/', views.delete_doctor, name='hospital-doctor-delete'),
    path('doctor/update/', views.update_doctor, name='hospital-doctor-update'),

    path('patient/', views.patient, name='hospital-patient'),
    path('patient/add/', views.add_patient, name='hospital-patient-add'),
    path('patient/update/', views.update_patients, name='hospital-patient-update'),
    path('patient/delete/', views.delete_patient, name='hospital-patient-delete'),
    path('visit/', views.visit, name='hospital-visit'),
    path('visit/add/', views.add_visit, name='hospital-visit-add'),
    path('visit/delete/', views.delete_visit, name='hospital-visit-delete'),
    path('visitprocess/', views.visit, name='hospital-v-process'),
    path('visit/add/process', views.add_visit_process, name='hospital-visit-add-process'),
    path('visit/delete/process', views.delete_visit_process, name='hospital-visit-delete-process'),
    path('diagnosis/', views.diagnosis, name='hospital-diagnosis'),
    path('diagnosis/add', views.add_diagnosis, name='hospital-diagnosis-add'),
    path('diagnosis/delete', views.delete_diagnosis, name='hospital-diagnosis-delete'),
    path('service/', views.service, name='hospital-service'),
    path('service/add', views.add_service, name='hospital-service-add'),
    path('service/delete', views.delete_service, name='hospital-service-delete'),


    # path('etc/', views.about, name='hospital-etc'),
]