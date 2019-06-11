from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def cdashboard(request):
    name = request.session['name']
    college = request.session['cname']
    email = request.session['email']
    return render(request,'campus/cdashboard.html',{'name': name})

def batch(request):
    return render(request,'campus/batch.html')

def company(request):
    return render(request,'campus/company.html')

def analysis(request):
    return render(request,'campus/analysis.html')

def cfeedback(request):
    return render(request,'campus/cfeedback.html')
