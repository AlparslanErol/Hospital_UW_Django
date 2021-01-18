from django.shortcuts import render
from django.http import HttpResponse

hospital = [
    {
        'name': 'LUXMED',
        'city': 'Warsaw',
    },
    {
        'name': 'Medical City',
        'city': 'Wroclaw',
    }
]



def index(request):
    return HttpResponse('<h1>Index</h1>')


def home(request):
    context = {'abc': hospital}
    return render(request, 'hospital/home.html', context)


def about(request):
    return render(request, 'hospital/about.html', {'title': 'About Title'})