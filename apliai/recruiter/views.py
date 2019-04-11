from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
# Database init
# Use a service account

db = firestore.client()
# Create your views here.

# Custom decorator need to see later
# def recruiter_login_required(function):
#     def _function(request,*args, **kwargs):
#         if request.session.get('user_type') == 'Recruiter':
#             return HttpResponseRedirect('recruiter/jobs')
#         else:
#             return HttpResponseRedirect('/')
#         return function(request, *args, **kwargs)
#     return _function


def dashboard(request):
    try:
        username = request.session['name']
        email = request.session['email']
        company_name = request.session['cname']
        user_type = request.session['user_type']
        print(username,email,company_name,user_type)
        return render(request,'recruiter/dashboard.html',{'name':username})
    except:
        return HttpResponseRedirect('/')


def jobs(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            # From post job form
            if request.method == "POST":
                try:
                    company_name = request.session['cname']
                    post = request.POST.get('post')
                    job_description = request.POST.get('jobdesc')
                    tskill = request.POST.getlist('tskill')
                    sskill = request.POST.getlist('sskill')
                    other = request.POST.getlist('other')
                    bond = request.POST.get('bond')
                    salary = request.POST.get('salary')
                    add_detail = request.POST.get('adddetail')
                    place = request.POST.get('place')                    
                    status = 'Opened'
                    jobid = request.session['email']+'$'+post+'$'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # print(company_name,post,job_description,tskill,sskill,other,bond,salary,add_detail,status,jobid,place)
                    doc_ref = db.collection(u'jobs').document(jobid)
                    doc_ref.set({
                        u'post': post,
                        u'job_description': job_description,
                        u'place':place,
                        u'tskill':tskill,
                        u'sskill':sskill,
                        u'other':other,
                        u'bond':bond,
                        u'salary':salary,
                        u'add_detail':add_detail,
                        u'status':status,
                        u'email':request.session['email']
                    })            
                    messages.success(request, 'Job posted successfully.')
                except:
                    messages.error(request, 'Something went wrong! Try Again Later.')    
            

            # get user data
            docs = db.collection(u'jobs').where(u'email',u'==',request.session['email']).get()
            jobs = []
            for doc in docs:
                # print(doc.to_dict())
                jobs.append(doc.to_dict())
            if not jobs:
                return render(request,'recruiter/jobs.html',{'new_user':'True','name':request.session['name']}) 
            else:
                return render(request,'recruiter/jobs.html',{'new_user':'False','jobs':jobs,'name':request.session['name']})              

    except:
        return HttpResponseRedirect('/')


def candidates(request):
    return render(request,'recruiter/candidates.html')


def team(request):
    return render(request,'recruiter/team.html')


def question(request):
    return render(request,'recruiter/question.html')


def feedback(request):
    return render(request,'recruiter/feedback.html')