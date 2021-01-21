from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.login, name='users-login'),
    path('register', views.register, name='users-register'),
    path('home/', views.home, name='users-home'),
]
