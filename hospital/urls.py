from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='hospital-home'),
    path('about', views.about, name='hospital-about'),
]