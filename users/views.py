from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from hospital.models import *
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%', '.', ',']
    val = True

    if len(passwd) < 6:
        print('length should be at least 6')
        val = False

    if len(passwd) > 20:
        print('length should be not be greater than 20')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val


def register(request):
    if request.method == 'POST' and password_check(request.POST['password']):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select id, name, surname
                        from doctor
                        UNION
                        select id, name, surname
                        from patient""")
        temp = cur.fetchall()
        member = Member(usernumber=request.POST['usernumber'], password=request.POST['password'],
                        name=request.POST['name'], surname=request.POST['surname'])
        for user in temp:
            if int(member.usernumber) == user['ID'] and member.name == user['NAME'] and member.surname == user['SURNAME']:
                member.save()
                break
            elif not(int(member.usernumber) == user['ID'] and member.name == user['NAME']
                     and member.surname == user['SURNAME']) and user != temp[-1]:
                continue
            else:
                print('\n!!!!!! Wrong registration attempt from {} {} !!!!!!\n'.format(user['NAME'], user['SURNAME']))
                context = {'msg': 'Your information and usernumber do not matched!'}
                return render(request, 'users/register.html', context)
        return redirect('/')
    else:
        context = {'msg':  'Password... \
                            Should have at least one number. \
                            Should have at least one uppercase and one lowercase character.\
                            Should have at least one special symbol.\
                            Should be between 6 to 20 characters long.!'}
        return render(request, 'users/register.html', context)


def login(request):
    request.session['admin_login'] = False
    request.session['patient_login'] = False
    request.session['doctor_login'] = False
    request.session['logged_in'] = False
    request.session['ID'] = None
    request.session['NAME'] = None
    request.session['SURNAME'] = None
    return render(request, 'users/login.html')


def home(request):
    try:
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""select *
                        from users_member
                        where usernumber = :number and password = :pass""", {'number': request.POST['usernumber'],
                                                                             'pass': request.POST['password']})
        temp = cur.fetchall()[0]
        member = Member(usernumber=temp['usernumber'], password=temp['password'],
                        name=temp['name'], surname=temp['surname'])
    except :
        member = False
        print("Exception... list index out of range!")

    if request.method == 'POST':
        if member:
            request.session['ID'] = member.usernumber
            request.session['NAME'] = member.name
            request.session['SURNAME'] = member.surname
            if member.is_admin():
                print('Admin account has been logged in!')
                request.session['admin_login'] = True
                request.session['logged_in'] = True
                return render(request, 'users/home.html', {'member': member})
            elif member.is_doctor():
                print('Doctor account has been logged in!')
                request.session['doctor_login'] = True
                request.session['logged_in'] = True
                return render(request, 'users/home.html', {'member': member})
            elif member.is_patient():
                print('Patient account has been logged in!')
                request.session['patient_login'] = True
                request.session['logged_in'] = True
                return render(request, 'users/home.html', {'member': member})
        else:
            context = {'msg': 'Invalid usernumber or password'}
            return render(request, 'users/login.html', context)
