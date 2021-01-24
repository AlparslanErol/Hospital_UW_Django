from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from hospital.models import *
import sqlite3


def dict_factory(cursor, row):
    """
    This method is used to convert tuple type to dict after execute SQL queries in python.
    :param cursor:
    :param row:
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def password_check(passwd):
    """
    Taken from geeksforgeeks.org/password-validation-in-python/
    This method is used to restrict password for registration process.
    :param passwd:
    :return:
    """
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
    """
    This method is for registration. Select id, name and surname of doctor and patient table and check their information
    If their id and information are not matched, system gives an error to register the system.
    Also to register system there are some restriction:
    Password...
    - Should have at least one number.
    - Should have at least one uppercase and one lowercase character.
    - Should have at least one special symbol.
    - Should be between 6 to 20 characters long.!
    Query Explanation:
    This query is to have id, name and surname data from doctor and patient.
    :param request:
    :return:
    """
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
    """
    For each login screen observe session parameters are given default values.
    :param request:
    :return:
    """
    request.session['admin_login'] = False
    request.session['patient_login'] = False
    request.session['doctor_login'] = False
    request.session['logged_in'] = False
    request.session['ID'] = None
    request.session['NAME'] = None
    request.session['SURNAME'] = None
    return render(request, 'users/login.html')


def home(request):
    """
    This method is use for after login credentials checked and user able to log into system,
    it method redirect the user to the home page with his/her name.
    Admin, doctor and patient session user parameters are updated after login process.
    with request.session['--'] parameter, we can keep who using the system in current time period and keep its log
    into the root file `logs.txt`
    :param request:
    :return:
    """
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
