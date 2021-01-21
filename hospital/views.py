from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import sqlite3


# Only Admin Access
def adm_login(func):
    def inner(request):
        if request.session['admin_login'] and request.session['logged_in']:
            return func(request)
        else:
            context = {'msg': 'Only admin accounts can access this link!'}
            request.session['logged_in'] = False
            return render(request, 'users/login.html', context)
    return inner


# Admin + Doctor Access
def adm_doc_login(func):
    def inner(request):
        if (request.session['admin_login'] or request.session['doctor_login']) and request.session['logged_in']:
            return func(request)
        else:
            context = {'msg': 'Only Admin + Doctor accounts can access this link!'}
            request.session['logged_in'] = False
            return render(request, 'users/login.html', context)
    return inner


# Admin + Patient Access
def adm_pat_login(func):
    def inner(request):
        if (request.session['patient_login'] or request.session['admin_login']) and request.session['logged_in']:
            return func(request)
        else:
            context = {'msg': 'Only Admin + Patient accounts can access this link!'}
            request.session['logged_in'] = False
            return render(request, 'users/login.html', context)
    return inner


# Admin + Doctor + Patient Access
def all_login(func):
    def inner(request):
        if (request.session['patient_login'] or request.session['admin_login'] or request.session['doctor_login']) \
                and request.session['logged_in']:
            return func(request)
        else:
            context = {'msg': 'All accounts can access this link!'}
            request.session['logged_in'] = False
            return render(request, 'users/login.html', context)
    return inner


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def is_logged_in(request):
    return request.session['logged_in'] == True


@all_login
def diagnosis(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select * from Diagnosis""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        con.close()
        return render(request, 'hospital/view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_doc_login
def doctor(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select * from Doctor""")
        temp = cur.fetchall()
        context = {
            'abc': temp,
        }
        con.close()
        return render(request, 'hospital/view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def patient(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select * from patient""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/patient_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@all_login
def service(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select * from service""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_doc_login
def visit(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select * from visit""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_doc_login
def visit_process(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select * from visit_process""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@all_login
def index(request):
    return HttpResponse('<h1>Index</h1>')


@all_login
def home(request):
    if is_logged_in(request):
        return render(request, 'hospital/home.html', {'title': 'About Title'})
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@all_login
def about(request):
    if is_logged_in(request):
        return render(request, 'hospital/about.html', {'title': 'About Title'})
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def add_doctor(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""insert into doctor values (:id,:name,:surname,:dept,NULL,NULL,NULL,NULL,NULL)""",
                    {'id': request.POST['ID'], 'name': request.POST['NAME'], 'surname': request.POST['SURNAME'],
                     'dept': request.POST['DEPARTMENT']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_doctor.html')


@adm_login
def add_patient(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""insert into patient values (:id,:name,:surname,NULL,NULL,NULL,NULL)""",
                    {'id': request.POST['ID'], 'name': request.POST['NAME'], 'surname': request.POST['SURNAME']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_patient.html')