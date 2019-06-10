from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def dashboard(request):
    name = request.session['name']
    college = request.session['cname']
    email = request.session['email']
    return render(request,'campus/dashboard.html',{'name': name})

def batch(request):
    return render(request,'campus/batch.html')

def company(request):
    return render(request,'campus/company.html')

def analysis(request):
    return render(request,'campus/analysis.html')

def feedback(request):
    return render(request,'campus/feedback.html')
