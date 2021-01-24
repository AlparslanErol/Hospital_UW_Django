from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import sqlite3
from matplotlib import pyplot as plt


# Only Admin Access
def adm_login(func):
    """
    This method is used to give authentication for only admin accounts
    :param func:
    :return:
    """
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
    """
    This method is used to give authentication for admin and doctor accounts
    :param func:
    :return:
    """
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
    """
    This method is used to give authentication for admin and patient accounts
    :param func:
    :return:
    """
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
    """
    This method is used to give authentication for all type of accounts
    :param func:
    :return:
    """
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
    """
    This method is used to convert tuple output from cursor to dictionary.
    :param cursor:
    :param row:
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def is_logged_in(request):
    """
    This method is used to check if user logged in or not.
    :param request:
    :return:
    """
    return request.session['logged_in'] == True


@all_login
def diagnosis(request):
    """
    In this method, diagnosis table is viewing via database connection.
    Query Explanation:
    This query is take all data from diagnosis table.
    :param request:
    :return:
    """
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
    """
    In this method, doctor table is viewing via database connection.
    Query Explanation:
    This query is take all data from doctor table.
    :param request:
    :return:
    """
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
    """
    In this method, patient table is viewing via database connection.
    Query Explanation:
    This query is take all data from patient table.
    :param request:
    :return:
    """
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
    """
    In this method, service table is viewing via database connection.
    Query Explanation:
    This query is take all data from service table.
    :param request:
    :return:
    """
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
    """
    In this method, visit table is viewing via database connection.
    Query Explanation:
    This query is take all data from visit table.
    :param request:
    :return:
    """
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
    """
    In this method, visit_process table is viewing via database connection.
    Query Explanation:
    This query is take all data from visit_process table.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show salary information from database.
    Query Explanation:
    If user is a doctor, query only gives result for this doctor salary.
    If user is an admin, query only gives all doctor's salary information.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show advanced sql queries from database.
    Query Explanation:
    Select average salary for every doctor title with count of visit process diagnosis is cancer greater than 2.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show advanced sql queries from database.
    Query Explanation:
    Select doctors who have maximum salary in each title and show them with additional column and put '*' sign,
    otherwise ' '
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show advanced sql queries from database.
    Query Explanation:
    Select patients whose names are not include ‘e’ or select patients who have visit type as 'inpatient' or
    select male patients who have and have doctor with salary greater than 5000.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show advanced sql queries from database.
    Query Explanation:
    Select total service cost in March 2020.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show advanced sql queries from database.
    Query Explanation:
    Select visit processes and information about patients who use service unit price greater than 100 with
    yearly income of their doctors who has professor title.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show advanced sql queries from database.
    Query Explanation:
    Select all each diagnosis for youngest female patients.
    :param request:
    :return:
    """
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
    """
    In this method, a view created to show results of patient's ongoing visit processes from database.
    If user is a patient, user can only observe his/her results.
    Else, user can see all visit processes results.
    Query Explanation:
    Select all each diagnosis for youngest female patients.
    :param request:
    :return:
    """
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
    """
    In this method, there are several sql queries to visualize the statistics about hospital with python matplotlib package.
    1. Count patients for each gender in patient table.
    2. Count doctors for each department in doctor table.
    3. Count doctors for each title in doctor table.
    4. Count visit processes for each diagnosis in visit process table.
    5. Count visit processes for each date in visit process table.
    Query Explanation:
    Select all each diagnosis for youngest female patients.
    :param request:
    :return:
    """
    if is_logged_in(request):
        con = sqlite3.connect("Hospital.db")
        con.row_factory = dict_factory
        cur = con.cursor()

        # STAT 1
        cur.execute(""" select gender, count(id)
                        from patient
                        group by gender;""")
        temp = cur.fetchall()
        new_dict = {}
        for stat in temp:
            new_dict[stat['GENDER']] = stat['count(id)']
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(new_dict.values(), explode=explode, labels=new_dict.keys(), autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('hospital/static/picture/piechart.png', dpi=100)

        # STAT 2
        cur.execute(""" select department, count(id) 
                        from doctor
                        group by department;""")
        temp = cur.fetchall()
        new_dict = {}
        for stat in temp:
            new_dict[stat['DEPARTMENT']] = stat['count(id)']
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(new_dict.values(), explode=explode, labels=new_dict.keys(), autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('hospital/static/picture/piechart_dept.png', dpi=100)

        # STAT 3
        cur.execute(""" select title, count(id) 
                        from doctor
                        group by title;""")
        temp = cur.fetchall()
        new_dict = {}
        for stat in temp:
            new_dict[stat['TITLE']] = stat['count(id)']
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(new_dict.values(), explode=explode, labels=new_dict.keys(), autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('hospital/static/picture/piechart_title.png', dpi=100)

        # STAT 4
        cur.execute(""" SELECT D.NAME, COUNT(VP.ID)
                        FROM VISIT_PROCESS VP, DIAGNOSIS D
                        WHERE VP.DIAGNOSIS_ID = D.ID
                        GROUP BY DIAGNOSIS_ID;""")
        temp = cur.fetchall()
        print(temp)
        new_dict = {}
        for stat in temp:
            new_dict[stat['NAME']] = stat['COUNT(VP.ID)']
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        explode = (0, 0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(new_dict.values(), explode=explode, labels=new_dict.keys(), autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('hospital/static/picture/piechart_diagnosis.png', dpi=100)

        # STAT 5
        cur.execute(""" SELECT PROCESS_DATE, COUNT(ID)
                        FROM VISIT_PROCESS
                        GROUP BY PROCESS_DATE;""")
        temp = cur.fetchall()
        print(temp)
        new_dict = {}
        for stat in temp:
            new_dict[stat['PROCESS_DATE']] = stat['COUNT(ID)']

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.bar(new_dict.keys(),
               new_dict.values(),
               color='purple')

        ax.set(xlabel="Date",
               ylabel="Process Count",
               title="Daily Total Process\nHospital UW, Warsaw.")
        plt.setp(ax.get_xticklabels(), rotation=45)
        plt.savefig('hospital/static/picture/bar_date_count.png', dpi=200)

        return render(request, 'hospital/piechart.html')
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@all_login
def home(request):
    """
    This method is used to show home page based on base.html
    :param request:
    :return:
    """
    if is_logged_in(request):
        return render(request, 'hospital/home.html', {'title': 'About Title'})
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@all_login
def about(request):
    """
    This method is used to show about page based on base.html
    :param request:
    :return:
    """
    if is_logged_in(request):
        return render(request, 'hospital/about.html', {'title': 'About Title'})
    else:
        context = {'msg': 'You have to log in first!'}
        return render(request, 'users/login.html', context)


@adm_login
def add_doctor(request):
    """
    This method is used to add doctor in doctor table.
    Query Explanation:
    - Insert data in doctor table.
    :param request:
    :return:
    """
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
    """
    This method is used to add patient in patient table.
    Query Explanation:
    - Insert data in patient table.
    :param request:
    :return:
    """
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
    """
    This method is used to add visit in visit table.
    Query Explanation:
    - Insert data in visit table.
    :param request:
    :return:
    """
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
    """
    This method is used to add visit_process in visit_process table.
    Query Explanation:
    - Insert data in visit_process table.
    :param request:
    :return:
    """
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
    """
    This method is used to add diagnosis in diagnosis table.
    Query Explanation:
    - Insert data in diagnosis table.
    :param request:
    :return:
    """
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
    """
    This method is used to add service in service table.
    Query Explanation:
    - Insert data in service table.
    :param request:
    :return:
    """
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
    """
    This method is used to delete doctor data in doctor table.
    Query Explanation:
    - Delete data in doctor table.
    :param request:
    :return:
    """
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
    """
    This method is used to delete patient data in patient table.
    Query Explanation:
    - Delete data in patient table.
    :param request:
    :return:
    """
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
    """
    This method is used to delete visit data in visit table.
    Query Explanation:
    - Delete data in visit table.
    :param request:
    :return:
    """
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
    """
    This method is used to delete visit_process data in visit_process table.
    Query Explanation:
    - Delete data in visit_process table.
    :param request:
    :return:
    """
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
    """
    This method is used to delete diagnosis data in diagnosis table.
    Query Explanation:
    - Delete data in diagnosis table.
    :param request:
    :return:
    """
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
    """
    This method is used to delete service data in service table.
    Query Explanation:
    - Delete data in service table.
    :param request:
    :return:
    """
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
    """
    This method is used to update doctor off day.
    Query Explanation:
    If user is a doctor, his/her usernumber keep in the session and doctor just write which day he/she wants to update.
    This query has been written to to update off_day in doctor table.
    :param request:
    :return:
    """
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
    """
    This method is used to update patient phone number.
    Query Explanation:
    If user is a patient, his/her usernumber keep in the session and patient just write phone number that  he/she wants to update.
    This query has been written to to update phone in patient table.
    :param request:
    :return:
    """
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
    """
    This method is used to update visit_process diagnosis number.
    Query Explanation:
    If user is a doctor, his/her usernumber keep in the session and doctor only eliglible to update his/her patient's diagnosis no for other doctor's patients.
    First query is to have visit process id for user doctor.
    Second query updates the diagnosis id in visit process table.
    If user is an admin, admin can update the table anyway.

    This method is also important that, it check the all diagnosis for each visit id and if all processes are done,
    State feature in Visit table has been updated automatically without any interrupt.
    First query is to count the diagnosis id for each visit
    Second query is to count the diagnosis id for each visit for diagnosis_id not equal to zero.
    If these two query results are equal, then visit table has been updated if not, no update.
    :param request:
    :return:
    """
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
    """
    This method is used to update salary feature in doctor table.
    Only admin account have access.
    Query Explanation:
    This query is used to update salary for given id number.
    :param request:
    :return:
    """
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
    """
    This method is used to update price feature in service table.
    Only admin account have access.
    Query Explanation:
    This query is used to update price for given id number.
    :param request:
    :return:
    """
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
