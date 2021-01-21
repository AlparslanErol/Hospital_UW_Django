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
        return render(request, 'hospital/visit_view.html', context)
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
        cur.execute("""insert into doctor values (:id,:name,:surname,:dept,:title,:email,:phone,:salary,:off_day)""",
                    {'id': request.POST['ID'], 'name': request.POST['NAME'], 'surname': request.POST['SURNAME'],
                     'dept': request.POST['DEPARTMENT'],'title': request.POST['TITLE'], 'email': request.POST['EMAIL'], 'phone': request.POST['PHONE'],
                     'salary': request.POST['SALARY'], 'off_day': request.POST['OFF_DAY']})
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
        cur.execute("""insert into patient values (:id,:name,:surname,:gender,:birthdate,:email,:phone)""",
                    {'id': request.POST['ID'], 'name': request.POST['NAME'], 'surname': request.POST['SURNAME'],
                     'gender': request.POST['GENDER'], 'birthdate': request.POST['BIRTHDATE'], 'email': request.POST['EMAIL'], 'phone': request.POST['PHONE']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_patient.html')


@adm_login
def add_visit(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""insert into visit values (:id,:doctor_id,:patient_id,:type,:date,:state)""",
                    {'id': request.POST['ID'], 'doctor_id': request.POST['DOCTOR_ID'], 'patient_id': request.POST['PATIENT_ID'],
                     'type': request.POST['TYPE'], 'date': request.POST['DATE'], 'state': request.POST['STATE']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_visit.html')


@adm_doc_login
def add_visit_process(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""insert into visit_process values (:id,:visit_id,:service_id,:diagnosis_id,:process_date,)""",
                    {'id': request.POST['ID'], 'visit_id': request.POST['VISIT_ID'], 'service_id': request.POST['SERVICE_ID'],
                     'diagnosis_id': request.POST['DIAGNOSIS_ID'], 'process_date': request.POST['PROCESS_DATE']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_visit_process.html')


@all_login
def add_diagnosis(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        for i in request.POST:
            print(i)
        cur.execute("""insert into diagnosis values (:id,:name)""",
                    {'id': request.POST['ID'], 'name': request.POST['NAME']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_diagnosis.html')


@all_login
def add_service(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""insert into service values (:id,:name,:unit_price,:quantity)""",
                    {'id': request.POST['ID'], 'name': request.POST['NAME'], 'unit_price': request.POST['UNIT_PRICE'],
                     'quantity': request.POST['QUANTITY']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_service.html')


@adm_login
def delete_doctor(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""delete from doctor where id = :num""",
                    {'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/delete_doctor.html')


@adm_login
def delete_patient(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""delete from patient where id = :num""",
                    {'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/delete_patient.html')


@adm_login
def delete_visit(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""delete from visit where id = :num""",
                    {'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/delete_visit.html')


@adm_login
def delete_visit_process(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""delete from visit_process where id = :num""",
                    {'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/delete_visit_process.html')


@adm_login
def delete_diagnosis(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""delete from diagnosis where id = :num""",
                    {'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/delete_diagnosis.html')


@adm_login
def delete_service(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""delete from service where id = :num""",
                    {'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/delete_service.html')


@all_login
def update_doctor(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""update doctor set off_day = :day where id = :num""",
                    {'day': request.POST['OFF_DAY'], 'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/update_doctor.html')


def update_patients(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""update patient set phone = :phone where id = :num""",
                    {'phone': request.POST['PHONE'], 'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/update_patient.html')














