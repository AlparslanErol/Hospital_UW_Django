from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import sqlite3
from matplotlib import pyplot as plt


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
        return render(request, 'hospital/diagnosis_view.html', context)
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


@adm_doc_login
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
        return render(request, 'hospital/service.html', context)
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
        return render(request, 'hospital/visit_process.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_doc_login
def salary(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        if request.session['doctor_login']:
            cur.execute("""select * from Doctor where id = :num""", {'num': request.session['ID']})
        else:
            cur.execute("""select * from Doctor""" )
        temp = cur.fetchall()
        context = {
            'abc': temp,
        }
        con.close()
        return render(request, 'hospital/salary.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def adv_1(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""SELECT D.TITLE,
                           AVG(D.SALARY) AVERAGE_SALARY
                      FROM PATIENT P,
                           VISIT V,
                           DOCTOR D,
                           VISIT_PROCESS VP,
                           DIAGNOSIS DI
                     WHERE V.DOCTOR_ID = D.ID AND 
                           V.PATIENT_ID = P.ID AND 
                           VP.VISIT_ID = V.ID AND 
                           VP.DIAGNOSIS_ID = DI.ID AND 
                           DI.NAME IN ('CANCER') 
                     GROUP BY D.TITLE
                        HAVING COUNT(VP.ID) >= 2;""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/adv_1_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def adv_2(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""SELECT NAME,
                           SURNAME,
                           TITLE,
                           SALARY,
                           '*' MAX_IN_TITLE
                      FROM DOCTOR
                     WHERE (SALARY, TITLE) IN (
                               SELECT MAX(SALARY),
                                      TITLE
                                 FROM DOCTOR
                                GROUP BY TITLE
                           )
                    UNION
                    SELECT NAME,
                           SURNAME,
                           TITLE,
                           SALARY,
                           ' ' MAX_IN_TITLE
                      FROM DOCTOR
                     WHERE (SALARY, TITLE) NOT IN (
                               SELECT MAX(SALARY),
                                      TITLE
                                 FROM DOCTOR
                                GROUP BY TITLE);""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/adv_2_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def adv_3(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""SELECT P.NAME PATIENT_NAME,
                               P.SURNAME PATIENT_SURNAME,
                               V.TYPE VISIT_TYPE
                          FROM PATIENT P,
                               VISIT V
                         WHERE V.PATIENT_ID = P.ID AND 
                               P.NAME NOT LIKE '%E%'
                        UNION
                        SELECT P.NAME PATIENT_NAME,
                               P.SURNAME PATIENT_SURNAME,
                               V.TYPE VISIT_TYPE
                          FROM PATIENT P,
                               VISIT V
                         WHERE V.PATIENT_ID = P.ID AND 
                               V.TYPE IN ('OUTPATIENT') 
                        UNION
                        SELECT P.NAME PATIENT_NAME,
                               P.SURNAME PATIENT_SURNAME,
                               V.TYPE VISIT_TYPE
                          FROM PATIENT P,
                               VISIT V,
                               DOCTOR D
                         WHERE V.PATIENT_ID = P.ID AND 
                               V.DOCTOR_ID = D.ID AND 
                               P.GENDER = 'MALE' AND 
                               D.SALARY > 5000""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/adv_3_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def adv_4(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""    SELECT SUM(S.UNIT_PRICE * S.QUANTITY) MARCH_2020_COST
                              FROM VISIT_PROCESS VP,
                                   SERVICE S
                             WHERE VP.SERVICE_ID = S.ID AND 
                                   VP.PROCESS_DATE BETWEEN '2020-03-01' AND '2020-04-01';""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/adv_4_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def adv_5(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""SELECT VP.ID PROCESS_NUMBER,
                               D.NAME DOCTOR_NAME,
                               D.SURNAME DOCTOR_SURNAME,
                               (D.SALARY * 12) DOCTOR_INCOME,
                               P.NAME PATIENT_NAME,
                               P.SURNAME PATIENT_SURNAME,
                               S.NAME SERVICE_NAME,
                               S.UNIT_PRICE * S.QUANTITY AS PRICE,
                               DI.NAME DIAGNOSIS_NAME
                          FROM SERVICE S,
                               PATIENT P,
                               VISIT V,
                               DOCTOR D,
                               VISIT_PROCESS VP,
                               DIAGNOSIS DI
                         WHERE V.DOCTOR_ID = D.ID AND 
                               V.PATIENT_ID = P.ID AND 
                               VP.VISIT_ID = V.ID AND 
                               VP.DIAGNOSIS_ID = DI.ID AND 
                               DI.NAME = 'COVID-19' AND 
                               D.TITLE = 'PROFESSOR' AND 
                               S.UNIT_PRICE > 100""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/adv_5_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def adv_6(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""SELECT DISTINCT (DI.NAME) DIAGNOSIS_NAME,
                                        PA.NAME PATIENT_NAME,
                                        PA.SURNAME PATIENT_SURNAME,
                                        PA.BIRTHDATE
                          FROM DIAGNOSIS DI,
                               VISIT_PROCESS VP,
                               VISIT V,
                               PATIENT PA
                         WHERE VP.VISIT_ID = V.ID AND 
                               VP.DIAGNOSIS_ID = DI.ID AND 
                               V.PATIENT_ID = PA.ID AND 
                               PA.ID IN (
                                   SELECT P.ID
                                     FROM PATIENT P
                                    WHERE P.BIRTHDATE = (
                                                            SELECT MAX(BIRTHDATE) 
                                                              FROM PATIENT
                                                             WHERE PATIENT.GENDER IN ('FEMALE') 
                                                        )
                                   )""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/adv_6_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@all_login
def results(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        if request.session['patient_login']:
            cur.execute("""SELECT VP.ID PROCESS_NUMBER,
                           D.NAME DOCTOR_NAME,
                           D.SURNAME DOCTOR_SURNAME,
                           P.NAME PATIENT_NAME,
                           P.SURNAME PATIENT_SURNAME,
                           S.NAME SERVICE_NAME,
                           S.UNIT_PRICE * S.QUANTITY AS PRICE,
                           DI.NAME DIAGNOSIS_NAME,
                           V.STATE
                      FROM SERVICE S,
                           PATIENT P,
                           VISIT V,
                           DOCTOR D,
                           VISIT_PROCESS VP,
                           DIAGNOSIS DI
                     WHERE V.DOCTOR_ID = D.ID AND 
                           V.PATIENT_ID = P.ID AND 
                           VP.VISIT_ID = V.ID AND 
                           VP.DIAGNOSIS_ID = DI.ID AND
                           P.ID = :id;""", {'id': request.session['ID']})
        else:
            cur.execute("""SELECT VP.ID PROCESS_NUMBER,
                           D.NAME DOCTOR_NAME,
                           D.SURNAME DOCTOR_SURNAME,
                           P.NAME PATIENT_NAME,
                           P.SURNAME PATIENT_SURNAME,
                           S.NAME SERVICE_NAME,
                           S.UNIT_PRICE * S.QUANTITY AS PRICE,
                           DI.NAME DIAGNOSIS_NAME,
                           V.STATE
                      FROM SERVICE S,
                           PATIENT P,
                           VISIT V,
                           DOCTOR D,
                           VISIT_PROCESS VP,
                           DIAGNOSIS DI
                     WHERE V.DOCTOR_ID = D.ID AND 
                           V.PATIENT_ID = P.ID AND 
                           VP.VISIT_ID = V.ID AND 
                           VP.DIAGNOSIS_ID = DI.ID""")
        temp = cur.fetchall()
        context = {
            'abc': temp
        }
        return render(request, 'hospital/result_view.html', context)
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_doc_login
def stats(request):
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(""" select gender, count(id)
                        from patient
                        group by gender;""")
        temp = cur.fetchall()
        new_dict = {}
        for stat in temp:
            new_dict[stat['GENDER']] = stat['count(id)']
        print(new_dict)
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(new_dict.values(), explode=explode, labels=new_dict.keys(), autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('hospital/static/picture/piechart.png', dpi=100)

        return render(request, 'hospital/piechart.html')
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
                     'dept': request.POST['DEPARTMENT'], 'title': request.POST['TITLE'], 'email': request.POST['EMAIL'],
                     'phone': request.POST['PHONE'],
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
                     'gender': request.POST['GENDER'], 'birthdate': request.POST['BIRTHDATE'],
                     'email': request.POST['EMAIL'], 'phone': request.POST['PHONE']})
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
                    {'id': request.POST['ID'], 'doctor_id': request.POST['DOCTOR_ID'],
                     'patient_id': request.POST['PATIENT_ID'],
                     'type': request.POST['TYPE'], 'date': request.POST['DATE'], 'state': request.POST['STATE']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_visit.html')


@adm_login
def add_visit_process(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""insert into visit_process values (:id,:visit_id,:service_id,:diagnosis_id,:process_date,)""",
                    {'id': request.POST['ID'], 'visit_id': request.POST['VISIT_ID'],
                     'service_id': request.POST['SERVICE_ID'],
                     'diagnosis_id': request.POST['DIAGNOSIS_ID'], 'process_date': request.POST['PROCESS_DATE']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/add_visit_process.html')


@adm_login
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


@adm_login
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


@adm_doc_login
def update_doctor(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""update doctor set off_day = :day where id = :num""",
                    {'day': request.POST['OFF_DAY'], 'num': request.session['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/update_doctor.html')


@adm_pat_login
def update_patients(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""update patient set phone = :phone where id = :num""",
                    {'phone': request.POST['PHONE'], 'num': request.session['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/update_patient.html')


@adm_doc_login
def update_visit_process(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()

        if request.session['doctor_login']:
            cur.execute(""" SELECT VP.ID
                            FROM VISIT_PROCESS VP, VISIT V
                            WHERE V.ID = VP.VISIT_ID AND V.DOCTOR_ID = :id""", {'id': request.session['ID']})
            temp = cur.fetchall()
            for val in temp:
                if request.POST['ID'] == str(val['ID']):
                    cur.execute("""update visit_process set diagnosis_id = :diagnosis where id = :num""",
                                {'diagnosis': request.POST['DIAGNOSIS'], 'num': request.POST['ID']})
        else:
            cur.execute("""update visit_process set diagnosis_id = :diagnosis where id = :num""",
                        {'diagnosis': request.POST['DIAGNOSIS'], 'num': request.POST['ID']})
        con.commit()

        cur.execute(""" SELECT COUNT(VISIT_PROCESS.ID) COUNT, VISIT_PROCESS.VISIT_ID V_ID
                        FROM VISIT, VISIT_PROCESS
                        WHERE VISIT.ID = VISIT_PROCESS.VISIT_ID AND VISIT_PROCESS.VISIT_ID = 
                        (SELECT VISIT_ID FROM VISIT_PROCESS WHERE ID = :num);""", {'num': request.POST['ID']})
        temp1 = cur.fetchall()
        cur.execute(""" SELECT COUNT(VISIT_PROCESS.ID) COUNT
                        FROM VISIT, VISIT_PROCESS
                        WHERE VISIT.ID = VISIT_PROCESS.VISIT_ID AND VISIT_PROCESS.DIAGNOSIS_ID != 0 
                        AND VISIT_PROCESS.VISIT_ID = (SELECT VISIT_ID FROM VISIT_PROCESS WHERE ID = :num)""",
                    {'num': request.POST['ID']})
        temp2 = cur.fetchall()

        if temp1[0]['COUNT'] == temp2[0]['COUNT']:
            cur.execute("""update visit set state = 2 where id = :num""", {'num': temp1[0]['V_ID']})

        con.commit()
        con.close()
        return render(request, 'hospital/home.html')
    else:
        context = {'msg': 'You can update only your patients statements!'}
        return render(request, 'hospital/update_visit_process.html', context)


@adm_login
def update_salary(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""update doctor set salary  = :salary where id = :num""",
                    {'salary': request.POST['SALARY'], 'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/update_salary.html')


@adm_login
def update_service(request):
    if request.method == 'POST':
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("""update service set unit_price  = :price where id = :num""",
                    {'price': request.POST['UNIT_PRICE'], 'num': request.POST['ID']})
        con.commit()
        cur.close()

        return render(request, 'hospital/home.html')
    else:
        return render(request, 'hospital/update_service.html')
