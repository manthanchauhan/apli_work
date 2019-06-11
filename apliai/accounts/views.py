from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
from . import emails
from string import ascii_lowercase, ascii_uppercase

# Database init
# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
# Powerful query not for developers
# docs = db.collection(u'users').get()
# for doc in docs:
#     db.collection(u'users').document(doc.id).set({u'user_type':'Company'},merge=True)

def reachus(request):
    if request.method == "POST":
        try:
            name = request.POST.get('emp_name')
            workplace = request.POST.get('company_name')
            work_email = request.POST.get('company_email')
            user_type = request.POST.get('user_type')
            if request.POST.get('emp_num') == '':
                # print(emp_name,company_name,company_email,"None")
                doc_ref = db.collection(u'reachus').document(work_email)
                doc_ref.set({
                    u'name': name,
                    u'workplace': workplace,
                    u'user_type':user_type
                })
                contact = '-'
            else:
                contact = request.POST.get('emp_num')
                # print(emp_name,company_name,company_email,emp_num)
                doc_ref = db.collection(u'reachus').document(work_email)
                doc_ref.set({
                    u'name': name,
                    u'workplace': workplace,
                    u'user_type':user_type,
                    u'contact': contact
                })
            email_from = settings.EMAIL_HOST_USER
            emails.mail(email_from, work_email)
            emails.mail2(workplace, work_email, name, str(contact),user_type)
            messages.success(request, 'Form submitted successfully, you will be contacted soon.')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/reachus.html')


def login(request):
    if request.method == "POST":
        try:
            email = request.POST.get('inputEmail')
            password = request.POST.get('inputPassword')
            if db.collection(u'users').document(email).get().exists:
                # user exists
                req = db.collection(u'users').document(email).get().to_dict()
                password_check = req['password']
                user_type = req['user_type']
                if password == password_check:
                    if user_type == 'Company':
                        role = req['role']
                        # session start
                        request.session['name'] = req['name']
                        request.session['email'] = email
                        request.session['cname'] = req['company_name']

                        if role == 'Recruiter':
                            request.session['role'] = 'Recruiter'
                        if role == 'Interviewer':
                            request.session['role'] = 'Interviewer'
                            request.session['parent'] = req['parent']
                        if role == 'Librarian':
                            request.session['role'] = 'Librarian'
                            request.session['parent'] = req['parent']
                        if role == 'Staff':
                            request.session['role'] = 'Staff'
                            request.session['parent'] = req['parent']
                        return HttpResponseRedirect('/recruiter/dashboard')
                    if user_type == 'Campus':
                        request.session['name'] = req['name']
                        request.session['email'] = email
                        request.session['cname'] = req['college']
                        return HttpResponseRedirect('/campus/cdashboard')
                    if user_type == 'Admin':
                        request.session['name'] = req['name']
                        request.session['email'] = email
                        return HttpResponseRedirect('/maintainer/mdashboard')
                else:
                    messages.error(request, 'Incorrect Password')
            else:
                messages.error(request, 'No such Account. Please Proceed to Reach Us')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/login.html')


def signup(request):
    if request.method == "POST":
        try:
            email = request.POST.get('inputEmail')
            password = request.POST.get('inputPassword')
            if (not db.collection(u'users').document(email).get().exists):
                # print(email,password)
                request.session['email'] = email
                request.session['password'] = password
                return render(request, 'accounts/step1.html')
            else:
                messages.error(request, 'Email already exists.Proceed to login')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/signup.html')


def step1(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            # print(name)    
            request.session['name'] = name
            return render(request, 'accounts/step2.html', {'name': name})
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/step1.html')


def step2(request):
    if request.method == "POST":
        try:
            cname = request.POST.get('cname')
            # print(cname)    
            request.session['cname'] = cname
            return render(request, 'accounts/step3.html', {'name': request.session['name'], 'cname': cname})
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/step2.html')


def step3(request):
    if request.method == "POST":
        try:
            position = request.POST.get('inlineRadioOptions')
            # print(role)    
            email = request.session['email']
            password = request.session['password']
            name = request.session['name']
            cname = request.session['cname']
            doc_ref = db.collection(u'users').document(email)
            doc_ref.set({
                u'name': name,
                u'company_name': cname,
                u'password': password,
                u'position': position,
                u'role': 'Recruiter',
                u'user_type':'Company'
            })
            db.collection(u'users').document(email).collection(
                u'packages').document(u'sample').set({u'id': 'sample'})
            messages.success(request, 'Signup completed successfully.')
            emails.mail3(email)
            return render(request, 'accounts/login.html')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/step3.html')

def campus_signup(request):
    if request.method == "POST":
        try:
            college_name = request.POST.get('cname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('uname')
            if (not db.collection(u'users').document(email).get().exists):
                doc_ref = db.collection(u'users').document(email)
                doc_ref.set({
                    u'name': name,
                    u'college': college_name,
                    u'password': password,
                    u'user_type':'Campus'
                })
                messages.success(request, 'Signup completed successfully.')
            return render(request, 'accounts/login.html')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/campus_signup.html')


def teamsignup(request, encodeddata):
    encodeddatareceived = "{}".format(encodeddata)
    pass_phrase = 'E7rtQhHyMPriyam'
    used = {' ', '\n'}
    key = []
    for c in pass_phrase.lower() + ascii_lowercase:
        if c not in used:
            key.append(c)
            used.add(c)
    key = ''.join(key)
    decode = {v: u for u, v in zip(ascii_lowercase, key)}
    list = encodeddatareceived.split('$')
    print(list)
    decodedrecmail = ''.join([decode.get(c, c) for c in list[1].lower()])
    decodedrole = ''.join([decode.get(c, c) for c in list[2].lower()])
    decodedinvmail = ''.join([decode.get(c, c) for c in list[3].lower()])
    global recrmail
    recrmail = decodedrecmail
    global invrole
    invrole = decodedrole
    global invimail
    invimail = decodedinvmail
    params = {'recmail': decodedrecmail, 'role': decodedrole, 'invmail': decodedinvmail}
    return render(request, 'accounts/member_signup.html', params)


def teamsignupcomplete(request):
    try:
        try:
            if request.method == "POST":
                password = request.POST.get('password')
                name = request.POST.get('name')
                position = request.POST.get('position')
                member_info = db.collection(u'users').document(invimail).get().to_dict()
                company_name = db.collection(u'users').document(recrmail).get().to_dict()['company_name']
                print(password, name, position, invimail, member_info)
                if member_info['status'] == 'inactive':
                    print('inactive status')
                    db.collection(u'users').document(invimail).update({
                        'status': 'active',
                        'position': position,
                        'name': name,
                        'password': password,
                        'company_name': company_name,
                        'user_type':'Company'
                    })
                    return JsonResponse({"success": "true"})

                if member_info['status'] == 'active':
                    return JsonResponse({"success": "false"})
        except:
            return JsonResponse({"success": "false"})
    except:
        return HttpResponseRedirect('/')


def logout(request):
    request.session.flush()
    return render(request, 'apliai/index.html')


def forgot_password(request):
    if request.method == "POST":
        try:
            umail = request.POST.get('usermail')
            if (db.collection(u'users').document(umail).get().exists):
                emails.fmail(umail)
                messages.success(request,
                                 'An email with the password reset link has been sent to the email address specified.Please click on the reset link to reset your password.')
                return render(request, 'accounts/forgot_password.html')
            else:
                messages.error(request, 'There is no account associated with that email address.')
        except:
            import traceback
            traceback.print_exc()
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/forgot_password.html')


def reset_confirm(request, umail):
    usermail = "{}".format(umail)
    pass_phrase = 'E7rtQhHyMPriyam'
    used = {' ', '\n'}
    key = []
    for c in pass_phrase.lower() + ascii_lowercase:
        if c not in used:
            key.append(c)
            used.add(c)
    key = ''.join(key)
    decode = {v: u for u, v in zip(ascii_lowercase, key)}
    decmail = ''.join([decode.get(c, c) for c in usermail.lower()])
    global strmail
    strmail = decmail
    return render(request, 'accounts/reset_confirm_form.html')


def reset_password_successful(request):
    try:
        if request.method == "POST":
            password = request.POST.get('password')
            req = db.collection(u'users').document(strmail).get().to_dict()
            # print(req)
            doc_ref = db.collection(u'users').document(strmail)
            doc_ref.set({
                u'password': password,
            }, merge=True)
        messages.success(request, "Password Reset Successfully")
        return render(request, 'accounts/login.html')
    except:
        messages.error(request, "Oops! Something Went Wrong. Please Try again later!")
