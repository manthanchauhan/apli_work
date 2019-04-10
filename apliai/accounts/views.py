from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Database init
# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
    # Post query example
    # doc_ref = db.collection(u'users').document(u'alovelace')
    # doc_ref.set({
    #     u'first': u'Ada',
    #     u'last': u'Lovelace',
    #     u'born': 1815
    # })    

    # Get Query example
    # users_ref = db.collection(u'users')
    # docs = users_ref.get()

    # for doc in docs:
    #     print(u'{} => {}'.format(doc.id, doc.to_dict()))    

def reachus(request):
    if request.method == "POST":
        try:
            emp_name = request.POST.get('emp_name')
            company_name = request.POST.get('company_name')
            company_email = request.POST.get('company_email')           
            if request.POST.get('emp_num') == '':
                print(emp_name,company_name,company_email,"None")
                doc_ref = db.collection(u'reachus').document(company_email)
                doc_ref.set({
                    u'emp_name': emp_name,
                    u'company_name': company_name,
                })                
            else:
                emp_num = request.POST.get('emp_num')
                print(emp_name,company_name,company_email,emp_num)
                doc_ref = db.collection(u'reachus').document(company_email)
                doc_ref.set({
                    u'emp_name': emp_name,
                    u'company_name': company_name,
                    u'emp_num':emp_num
                })
            messages.success(request, 'Form submitted successfully, will contact you soon.')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/reachus.html')

def login(request):
    if request.method == "POST":
        try:
            email=request.POST.get('inputEmail')
            password=request.POST.get('inputPassword')
            if(db.collection(u'users').document(email).get().exists):
                # user exists
                print(email,password)
                password_check = db.collection(u'users').document(email).get().to_dict()['password']
                if(password == password_check):
                    messages.success(request, 'Login Successful')
                    return render(request,'recruiter/dashboard.html')
                else:
                    messages.error(request, 'Incorrect Password')
            else:
                messages.error(request, 'No such Account. Please Proceed to Reach Us')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/login.html')

def signup(request):
    if request.method == "POST":
        try:
            email=request.POST.get('inputEmail')
            password=request.POST.get('inputPassword')
            if(not db.collection(u'users').document(email).get().exists):
                print(email,password)
                request.session['email'] = email
                request.session['password'] = password
                return render(request,'accounts/step1.html')    
            else:
                messages.error(request, 'Email already exists.Proceed to login')                
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/signup.html')

def step1(request):
    if request.method == "POST":
        try:
            name=request.POST.get('name')
            print(name)    
            request.session['name'] = name
            return render(request,'accounts/step2.html',{'name':name})            
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/step1.html')

def step2(request):
    if request.method == "POST":
        try:
            cname=request.POST.get('cname')
            print(cname)    
            request.session['cname'] = cname
            return render(request,'accounts/step3.html',{'name':request.session['name'],'cname':cname})    
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/step2.html')

def step3(request):
    if request.method == "POST":
        try:
            role=request.POST.get('inlineRadioOptions')
            print(role)    
            email = request.session['email']
            password = request.session['password']
            name = request.session['name']
            cname = request.session['cname']
            doc_ref = db.collection(u'users').document(email)
            doc_ref.set({
                u'name': name,
                u'company_name': cname,
                u'password':password,
                u'role':role
            })
            messages.success(request, 'Signup completed successfully.')            

            return render(request,'accounts/login.html')    
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/step3.html')

def logout(request):
    return render(request,'apliai/index.html')