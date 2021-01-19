from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def diagnosis(request):
    con = sqlite3.connect("Hospital.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("""select * from Diagnosis""")
    temp = cur.fetchall()
    context = {
        'abc': temp
    }
    con.close()
    return render(request, 'hospital/home.html', context)


def doctor(request):
    con = sqlite3.connect("Hospital.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("""select * from Doctor""")
    temp = cur.fetchall()
    context = {
        'abc': temp
    }
    return render(request, 'hospital/home.html', context)


def patient(request):
    con = sqlite3.connect("Hospital.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("""select * from patient""")
    temp = cur.fetchall()
    context = {
        'abc': temp
    }
    return render(request, 'hospital/home.html', context)


def service(request):
    con = sqlite3.connect("Hospital.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("""select * from service""")
    temp = cur.fetchall()
    context = {
        'abc': temp
    }
    return render(request, 'hospital/home.html', context)


def visit(request):
    con = sqlite3.connect("Hospital.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("""select * from visit""")
    temp = cur.fetchall()
    context = {
        'abc': temp
    }
    return render(request, 'hospital/home.html', context)


def index(request):
    return HttpResponse('<h1>Index</h1>')


def home(request):
    context = {
        'abc': abc
    }
    return render(request, 'hospital/home.html', context)


def about(request):
    return render(request, 'hospital/about.html', {'title': 'About Title'})
