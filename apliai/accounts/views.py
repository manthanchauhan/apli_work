from django.shortcuts import render
from django.http import HttpResponse

def reachus(request):
    if request.method == "POST":
        emp_name = request.POST.get('emp_name')
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        if request.POST.get('emp_num') == '':
            print(emp_name,company_name,company_email,"None")
        else:
            emp_num = request.POST.get('emp_num')
            print(emp_name,company_name,company_email,emp_num)

    return render(request,'accounts/reachus.html')

def login(request):
    return render(request,'accounts/login.html')

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