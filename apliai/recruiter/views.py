from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
        print(username, email, company_name, user_type)
        return render(request, 'recruiter/dashboard.html', {'name': username})
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
                    jobid = request.session['email'] + '$' + post + '$' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # print(company_name,post,job_description,tskill,sskill,other,bond,salary,add_detail,status,jobid,place)
                    doc_ref = db.collection(u'jobs').document(jobid)
                    doc_ref.set({
                        u'post': post,
                        u'job_description': job_description,
                        u'place': place,
                        u'tskill': tskill,
                        u'sskill': sskill,
                        u'other': other,
                        u'bond': bond,
                        u'salary': salary,
                        u'add_detail': add_detail,
                        u'status': status,
                        u'email': request.session['email']
                    })
                    messages.success(request, 'Job posted successfully.')
                except:
                    messages.error(request, 'Something went wrong! Try Again Later.')

                    # get jobs data
            docs = db.collection(u'jobs').where(u'email', u'==', request.session['email']).get()
            jobs = []
            for doc in docs:
                # print(doc.to_dict())
                jobs.append(doc.to_dict())
            if not jobs:
                return render(request, 'recruiter/jobs.html', {'new_user': 'True', 'name': request.session['name']})
            else:
                return render(request, 'recruiter/jobs.html',
                              {'new_user': 'False', 'jobs': jobs, 'name': request.session['name']})

    except:
        return HttpResponseRedirect('/')


def candidates(request):
    # try:
    if request.session['user_type'] == 'Recruiter':
        # get jobs data
        docs = db.collection(u'candidates').where(u'company_name', u'==', request.session['cname']).get()
        jobs_posted = len(list(db.collection(u'jobs').where(u'email', u'==', request.session['email']).get()))
        applicants = []
        custom_dict = {}
        for doc in docs:
            custom_dict['candidate_name'] = doc.to_dict()['candidate_name']
            custom_dict['company_name'] = doc.to_dict()['company_name']
            custom_dict['resume'] = doc.to_dict()['resume']
            custom_dict['video_resume'] = doc.to_dict()['video_resume']
            custom_dict['grade'] = doc.to_dict()['grade']
            custom_dict['place'] = db.collection(u'jobs').document(doc.to_dict()['job_id'].id).get().to_dict()['place']
            custom_dict['post'] = db.collection(u'jobs').document(doc.to_dict()['job_id'].id).get().to_dict()['post']
            # print(custom_dict)
            applicants.append(custom_dict)
        if not applicants:
            return render(request, 'recruiter/candidates.html',
                          {'new_user': 'True', 'name': request.session['name'], 'appcount': 0, 'jobs_posted': 0, })
        else:
            return render(request, 'recruiter/candidates.html',
                          {'new_user': 'False', 'applicants': applicants, 'name': request.session['name'],
                           'appcount': len(applicants), 'jobs_posted': jobs_posted})

            # except:
    #     return HttpResponseRedirect('/')


def team(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            return render(request, 'recruiter/team.html')

    except:
        return HttpResponseRedirect('/')


def question(request):
    try:
        if request.session['user_type'] == 'Recruiter':

            user_packages_docs = db.collection(u'users').document(request.session['email']).collection(
                u'packages').get()
            user_packages = []
            for doc in user_packages_docs:
                print(doc.id)
                user_packages.append(doc.id)

            user_questions_docs = db.collection(u'users').document(request.session['email']).collection(
                u'packages').document('sample').collection(
                u'questions').get()
            user_questions = []
            for doc in user_questions_docs:
                # print(doc.to_dict())
                user_questions.append(doc.to_dict())

            built_in_questions_docs = db.collection(
                u'questions').get()
            built_in_questions = []
            for doc in built_in_questions_docs:
                # print(doc.to_dict())
                built_in_questions.append(doc.to_dict())

            return render(request, 'recruiter/question.html',
                          {'user_questions': user_questions, 'built_in_questions': built_in_questions,
                           'user_packages': user_packages})

    except:
        return HttpResponseRedirect('/')


def addpackage(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            # From post job form
            if request.method == "POST":
                try:
                    print('request for adding package')
                    packageName = request.POST.get('packageName')
                    question = request.POST.get('question')
                    questionType = request.POST.get('questionType')
                    db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).set({u'id': packageName})
                    doc_ref = db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).collection(
                        u'questions').document()
                    db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).collection(
                        u'questions').document(doc_ref.id).set({
                        u'id': doc_ref.id,
                        u'question': question,
                        u'type': questionType,
                    })
                    return JsonResponse({"success": "true"})
                except:
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def changepackage(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            # From post job form
            if request.method == "POST":
                try:
                    packageName = request.POST.get('packageName')
                    print('request for change package', packageName)

                    user_questions_docs = db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).collection(
                        u'questions').get()
                    user_questions = []
                    for doc in user_questions_docs:
                        # print(doc.to_dict())
                        user_questions.append(doc.to_dict())

                    return JsonResponse({"user_questions": user_questions})
                except:
                    return JsonResponse({"success": "false"})

    except:
        pass


def addquestion(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            # From post job form
            if request.method == "POST":
                try:
                    print('request for adding question')
                    packageName = request.POST.get('packageName')
                    question = request.POST.get('question')
                    questionType = request.POST.get('questionType')

                    doc_ref = db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).collection(
                        u'questions').document()
                    db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).collection(
                        u'questions').document(doc_ref.id).set({
                        u'id': doc_ref.id,
                        u'question': question,
                        u'type': questionType,
                    })
                    return JsonResponse({"success": "true"})
                except:
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def deletequestion(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            # From post job form
            if request.method == "POST":
                try:
                    id = request.POST.get('id')
                    packageName = request.POST.get('packageName')
                    print('deleting question with id=>', id, ' and package =>', packageName)

                    db.collection(u'users').document(request.session['email']).collection(
                        u'packages').document(packageName).collection(
                        u'questions').document(id).delete()
                    return JsonResponse({"success": "true"})
                except:
                    messages.error(request, 'Something went wrong! Try Again Later.')
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def feedback(request):
    try:
        if request.session['user_type'] == 'Recruiter':
            return render(request, 'recruiter/feedback.html')

    except:
        return HttpResponseRedirect('/')
