from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def login(request):
    return render(request,'accounts/login.html')

    # return HttpResponse("Login page working !")

def signup(request):
    return render(request,'accounts/signup.html')

def step1(request):
    return render(request,'accounts/step1.html')

def step2(request):
    return render(request,'accounts/step2.html')

def step3(request):
    return render(request,'accounts/step3.html')

def logout(request):
    return render(request,'apliai/index.html')