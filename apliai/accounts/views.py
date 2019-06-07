from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
from . import emails
from string import ascii_lowercase,ascii_uppercase
# Database init
# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def reachus(request):
    if request.method == "POST":
        try:
            emp_name = request.POST.get('emp_name')
            company_name = request.POST.get('company_name')
            company_email = request.POST.get('company_email')           
            if request.POST.get('emp_num') == '':
                # print(emp_name,company_name,company_email,"None")
                doc_ref = db.collection(u'reachus').document(company_email)
                doc_ref.set({
                    u'emp_name': emp_name,
                    u'company_name': company_name,
                })
                emp_num = '-'                
            else:
                emp_num = request.POST.get('emp_num')
                # print(emp_name,company_name,company_email,emp_num)
                doc_ref = db.collection(u'reachus').document(company_email)
                doc_ref.set({
                    u'emp_name': emp_name,
                    u'company_name': company_name,
                    u'emp_num':emp_num
                })
            email_from = settings.EMAIL_HOST_USER
            emails.mail(email_from,company_email)
            emails.mail2(company_name,company_email,emp_name,str(emp_num))
            messages.success(request, 'Form submitted successfully, you will be contacted soon.')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    docs = db.collection(u'users').get()
    return render(request,'accounts/reachus.html')

def login(request):
    if request.method == "POST":
        try:
            email=request.POST.get('inputEmail')
            password=request.POST.get('inputPassword')
            if(db.collection(u'users').document(email).get().exists):
                # user exists
                # print(email,password)
                req = db.collection(u'users').document(email).get().to_dict()
                password_check = req['password']
                if(password == password_check):
                    # session start
                    request.session['name'] = req['name']
                    request.session['email'] = email
                    request.session['cname'] = req['company_name']
                    request.session['user_type'] = 'Recruiter'                  
                    return HttpResponseRedirect('/recruiter/dashboard')
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
                # print(email,password)
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
            # print(name)    
            request.session['name'] = name
            return render(request,'accounts/step2.html',{'name':name})            
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/step1.html')

def step2(request):
    if request.method == "POST":
        try:
            cname=request.POST.get('cname')
            # print(cname)    
            request.session['cname'] = cname
            return render(request,'accounts/step3.html',{'name':request.session['name'],'cname':cname})    
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/step2.html')

def step3(request):
    if request.method == "POST":
        try:
            position=request.POST.get('inlineRadioOptions')
            # print(role)    
            email = request.session['email']
            password = request.session['password']
            name = request.session['name']
            cname = request.session['cname']
            doc_ref = db.collection(u'users').document(email)
            doc_ref.set({
                u'name': name,
                u'company_name': cname,
                u'password':password,
                u'position':position
            })
            messages.success(request, 'Signup completed successfully.')
            emails.mail3(email)
            return render(request,'accounts/login.html')    
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/step3.html')

def teamsignup(request,encodeddata):
    #all data is fetched and decoded here.you can proceed as you want in case of any query feel free to contact me    
    encodeddatareceived="{}".format(encodeddata)
    pass_phrase = 'APLIAI'
    used = {' ', '\n'}
    key = []
    for c in pass_phrase.lower() + ascii_lowercase:
        if c not in used:
              key.append(c)
              used.add(c)
    key = ''.join(key)
    decode = {v: u for u, v in zip(ascii_lowercase, key)}
    list=encodeddatareceived.split('$')
    print(list)
    decodedrecmail=''.join([decode.get(c, c) for c in list[1].lower()])
    decodedrole=''.join([decode.get(c, c) for c in list[2].lower()])
    decodedinvmail=''.join([decode.get(c, c) for c in list[3].lower()])
    global recrmail
    recrmail=decodedrecmail
    global invrole
    invrole=decodedrole
    global invimail
    invimail=decodedinvmail
    params={'recmail':decodedrecmail,'role':decodedrole,'invmail':decodedinvmail}
    return render(request,'accounts/member_signup.html',params)

def teamsignupcomplete(request):
    if request.method=="POST":
        email=request.POST.get('inputEmail')
        password=request.POST.get('inputPassword')
        name=request.POST.get('name')
        position =request.POST.get('inlineRadioOptions')
        recruiteremail=recrmail
        invitedemail=invimail
        invitedrole=invrole
        return HttpResponse("data feteched successfully . you can do your action from here.")

def logout(request):
    request.session.flush()
    return render(request,'apliai/index.html')

def forgot_password(request):
    if request.method=="POST":
        try:
            umail=request.POST.get('usermail')
            if(db.collection(u'users').document(umail).get().exists):
                emails.fmail(umail)
                messages.success(request,'An email with the password reset link has been sent to the email address specified.Please click on the reset link to reset your password.')
                return render(request,'accounts/forgot_password.html')
            else:
                messages.error(request, 'There is no account associated with that email address.')
        except:
            import traceback
            traceback.print_exc()
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request,'accounts/forgot_password.html')

def reset_confirm(request,umail):
    usermail="{}".format(umail)
    pass_phrase = 'E7rtQhHyMPriyam'
    used = {' ', '\n'}
    key = []
    for c in pass_phrase.lower() + ascii_lowercase:
        if c not in used:
              key.append(c)
              used.add(c)
    key = ''.join(key)
    decode = {v: u for u, v in zip(ascii_lowercase, key)}
    decmail=''.join([decode.get(c, c) for c in usermail.lower()])
    global strmail
    strmail=decmail
    return render(request,'accounts/reset_confirm_form.html')

def reset_password_successful(request):
    try:
        if request.method=="POST":
            password=request.POST.get('password')
            req = db.collection(u'users').document(strmail).get().to_dict()
            #print(req)
            doc_ref = db.collection(u'users').document(strmail)
            doc_ref.set({
                    u'password':password,
                },merge=True)
        messages.success(request,"Password Reset Successfully")
        return render(request,'accounts/login.html')
    except:
        messages.error(request,"Oops! Something Went Wrong. Please Try again later!")