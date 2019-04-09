from django.shortcuts import render
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Database init
# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

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
    # doc_ref = db.collection(u'users').document(u'alovelace')
    # doc_ref.set({
    #     u'first': u'Ada',
    #     u'last': u'Lovelace',
    #     u'born': 1815
    # })    
    return render(request,'accounts/reachus.html')

def login(request):
    if request.method == "POST":
        email=request.POST.get('inputEmail')
        password=request.POST.get('inputPassword')
        print(email,password)
    return render(request,'accounts/login.html')

def signup(request):
    if request.method == "POST":
        email=request.POST.get('inputEmail')
        password=request.POST.get('inputPassword')
        print(email,password)    
    return render(request,'accounts/signup.html')

def step1(request):
    if request.method == "POST":
        name=request.POST.get('name')
        print(name)    
    return render(request,'accounts/step1.html')

def step2(request):
    if request.method == "POST":
        cname=request.POST.get('cname')
        print(cname)    

    return render(request,'accounts/step2.html')

def step3(request):
    if request.method == "POST":
        role=request.POST.get('inlineRadioOptions')
        print(role)    
    return render(request,'accounts/step3.html')

def logout(request):
    return render(request,'apliai/index.html')