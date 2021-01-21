from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='hospital-home'),
    path('about/', views.about, name='hospital-about'),
    path('results/', views.results, name='hospital-results'),
    path('adv/1/', views.adv_1, name='hospital-adv-1'),
    path('adv/2/', views.adv_2, name='hospital-adv-2'),
    path('adv/3/', views.adv_3, name='hospital-adv-3'),
    path('adv/4/', views.adv_4, name='hospital-adv-4'),
    path('adv/5/', views.adv_5, name='hospital-adv-5'),
    path('adv/6/', views.adv_6, name='hospital-adv-6'),
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
    path('visitprocess/update/', views.update_visit_process, name='hospital-v-process-update'),
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