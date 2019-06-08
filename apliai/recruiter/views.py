from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from . import emails

# Database init
# Use a service account

db = firestore.client()


# Create your views here.

# Custom decorator need to see later
# def recruiter_login_required(function):
#     def _function(request,*args, **kwargs):
#         if request.session.get('role') == 'Recruiter':
#             return HttpResponseRedirect('recruiter/jobs')
#         else:
#             return HttpResponseRedirect('/')
#         return function(request, *args, **kwargs)
#     return _function


def dashboard(request):
    # try:
    if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
        'role'] == 'Interviewer' or request.session['role'] == 'Staff':
        print('current role is : ', request.session['role'])
        if request.session['role'] == 'Recruiter':
            main_email = request.session['email']
        else:
            print('current role is : ', request.session['role'])
            main_email = request.session['parent']
    company_name = request.session['cname']
    username = request.session['name']
    email = main_email
    role = request.session['role']
    print(username, email, company_name, role)
    return render(request, 'recruiter/dashboard.html', {'name': username, 'role': role})


# except:
#     return HttpResponseRedirect('/')


def jobs(request):
    try:
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Staff':
            main_email = request.session['email']
        else:
            print('current role is : ', request.session['role'])
            main_email = request.session['parent']
            # From post job form
        if request.method == "POST":
            try:
                company_name = request.session['cname']
                packageId = request.POST.get('userPackages')
                post = request.POST.get('post')
                job_description = request.POST.get('jobdesc')
                key_responsibility = request.POST.get('keyresp')
                tskill = request.POST.getlist('tskill')
                sskill = request.POST.getlist('sskill')
                other = request.POST.getlist('other')
                bond = request.POST.get('bond')
                salary = request.POST.get('salary')
                add_detail = request.POST.get('adddetail')
                place = request.POST.get('place')
                joining_date = request.POST.get('startdate')
                deadline = request.POST.get('deadline')
                status = 'Opened'
                jobid = main_email + '$' + post + '$' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print(company_name,post,job_description,tskill,sskill,other,bond,salary,add_detail,status,jobid,place,joining_date,deadline,key_responsibility)
                doc_ref = db.collection(u'jobs').document(jobid)
                doc_ref.set({
                    u'post': post,
                    u'job_description': job_description,
                    u'key_responsibility': key_responsibility,
                    u'place': place,
                    u'tskill': tskill,
                    u'sskill': sskill,
                    u'other': other,
                    u'start_date': joining_date,
                    u'deadline': deadline,
                    u'bond': bond,
                    u'salary': salary,
                    u'add_detail': add_detail,
                    u'status': status,
                    u'email': main_email,
                    u'packageId': packageId
                })
                messages.success(request, 'Job posted successfully.')
            except:
                messages.error(request, 'Something went wrong! Try Again Later.')

                # get jobs data
        docs = db.collection(u'jobs').where(u'email', u'==', main_email).get()
        jobs = []
        open_count = 0
        close_count = 0
        for doc in docs:
            # print(doc.to_dict())
            # print(doc.id)
            stat = doc.to_dict()['status']
            deadline = doc.to_dict()['deadline']
            if stat == 'Opened':
                if datetime.strptime(deadline, '%Y-%m-%d') < datetime.today():
                    db.collection(u'jobs').document(doc.id).set({u'status': 'Closed'}, merge=True)
                    doc.to_dict()['status'] = 'Closed'
                else:
                    open_count += 1
            temp = doc.to_dict()
            temp.update({'id': doc.id})
            # print(temp['id'])
            jobs.append(temp)

        user_packages_docs = db.collection(u'users').document(main_email).collection(
            u'packages').get()
        user_packages = []
        for doc in user_packages_docs:
            # print(doc.id)
            user_packages.append(doc.id)

        close_count = len(jobs) - open_count
        if not jobs:
            return render(request, 'recruiter/jobs.html',
                          {'role': request.session['role'], 'new_user': 'True', 'name': request.session['name'],
                           'jc': 0, 'oc': 0, 'cc': 0})
        else:
            return render(request, 'recruiter/jobs.html',
                          {'role': request.session['role'], 'new_user': 'False', 'jobs': jobs,
                           'name': request.session['name'], 'jc': len(jobs),
                           'oc': open_count, 'cc': close_count, 'user_packages': user_packages})

    except:
        return HttpResponseRedirect('/')


def deletepost(request):
    try:

        if request.session['role'] == 'Recruiter':
            # From post job form
            if request.method == "POST":
                try:
                    id = request.POST.get('id')
                    db.collection(u'jobs').document(id).delete()
                    messages.success(request, 'Post deleted successfully.')
                    return JsonResponse({"success": "true"})
                except:
                    messages.error(request, 'Something went wrong! Try Again Later.')
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def candidates(request):
    # try:
    if request.session['role'] == 'Recruiter' or request.session['role'] == 'Interviewer':
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
            custom_dict['resume_score'] = doc.to_dict()['resume_score']
            custom_dict['video_resume_score'] = doc.to_dict()['video_resume_score']
            custom_dict['grade'] = (custom_dict['resume_score'] + custom_dict['video_resume_score'])/2.0
            custom_dict['place'] = db.collection(u'jobs').document(doc.to_dict()['jobid'].id).get().to_dict()[
                'place']
            custom_dict['post'] = db.collection(u'jobs').document(doc.to_dict()['jobid'].id).get().to_dict()['post']
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
        if request.session['role'] == 'Recruiter':
            team_docs = db.collection(u'users').where(u'parent', u'==', request.session['email']).get()
            teams = []
            for doc in team_docs:
                # print(doc.id)
                teams.append(doc.to_dict())
            return render(request, 'recruiter/team.html',
                          {'role': request.session['role'], 'teams': teams, 'name': request.session['name']})

    except:
        return HttpResponseRedirect('/')


def deleteteamuser(request):
    try:
        if request.session['role'] == 'Recruiter':
            if request.method == "POST":
                try:
                    uid = request.POST.get('uid')
                    print('request for deleteing field of id=> ', uid)

                    db.collection(u'users').document(uid).delete()
                    return JsonResponse({"success": "true"})
                except:
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def inviteteamuser(request):
    try:
        if request.session['role'] == 'Recruiter':
            if request.method == "POST":
                try:
                    email = request.POST.get('email')
                    role = request.POST.get('role')
                    recmail = request.session['email']
                    rname = request.session['name']
                    print("inviteteamuser")
                    print("invmail: " + email)
                    print("rname: " + rname)
                    print("role: " + role)
                    print("recmail: " + recmail)
                    print('request for invite user => ', email, ' => ', role)
                    db.collection(u'users').document(email).set({
                        'parent': recmail,
                        'role': role,
                        'status': 'inactive',
                        'email': email
                    })
                    # write logic for send invite email here
                    emails.inmail(email, role, recmail, rname)
                    return JsonResponse({"success": "true"})
                except:
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def question(request):
    try:
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Staff':
            if request.session['role'] == 'Recruiter':
                main_email = request.session['email']
            else:
                print('current role is : ', request.session['role'])
                main_email = request.session['parent']
            user_packages_docs = db.collection(u'users').document(main_email).collection(
                u'packages').get()
            user_packages = []
            for doc in user_packages_docs:
                # print(doc.id)
                user_packages.append(doc.id)

            user_questions_docs = db.collection(u'users').document(main_email).collection(
                u'packages').document('sample').collection(
                u'questions').get()
            user_questions = []
            for doc in user_questions_docs:
                # print(doc.to_dict())
                user_questions.append(doc.to_dict())

            built_in_questions_docs = db.collection(
                u'questions').where(u'type', u'==', u'BEHAVIORAL').get()
            built_in_questions = []
            for doc in built_in_questions_docs:
                # print(doc.to_dict())
                built_in_questions.append(doc.to_dict())

            return render(request, 'recruiter/question.html',
                          {'role': request.session['role'], 'user_questions': user_questions,
                           'built_in_questions': built_in_questions,
                           'user_packages': user_packages, 'name': request.session['name']})

    except:
        return HttpResponseRedirect('/')


def addpackage(request):
    try:
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Staff':
            if request.session['role'] == 'Recruiter':
                main_email = request.session['email']
            else:
                print('current role is : ', request.session['role'])
                main_email = request.session['parent']
            # From post job form
            if request.method == "POST":
                try:
                    # print('request for adding package')
                    packageName = request.POST.get('packageName')
                    question = request.POST.get('question')
                    questionType = request.POST.get('questionType')
                    db.collection(u'users').document(main_email).collection(
                        u'packages').document(packageName).set({u'id': packageName})
                    doc_ref = db.collection(u'users').document(main_email).collection(
                        u'packages').document(packageName).collection(
                        u'questions').document()
                    db.collection(u'users').document(main_email).collection(
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
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Staff':
            if request.session['role'] == 'Recruiter':
                main_email = request.session['email']
            else:
                print('current role is : ', request.session['role'])
                main_email = request.session['parent']  # From post job form
            if request.method == "POST":
                try:
                    packageName = request.POST.get('packageName')
                    # print('request for change package', packageName)

                    user_questions_docs = db.collection(u'users').document(main_email).collection(
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


def loadquestions(request):
    try:
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Staff':
            if request.session['role'] == 'Recruiter':
                main_email = request.session['email']
            else:
                print('current role is : ', request.session['role'])
                main_email = request.session['parent']
                # From post job form
            if request.method == "POST":
                try:
                    questionType = request.POST.get('questionType')
                    print('request for change package', questionType)

                    built_in_questions_docs = db.collection(
                        u'questions').where(u'type', u'==', questionType).get()
                    built_in_questions = []
                    for doc in built_in_questions_docs:
                        # print(doc.to_dict())
                        built_in_questions.append(doc.to_dict())

                    return JsonResponse({"built_in_questions": built_in_questions})
                except:
                    return JsonResponse({"success": "false"})

    except:
        pass


def addquestion(request):
    # try:
    if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
        'role'] == 'Staff':
        if request.session['role'] == 'Recruiter':
            main_email = request.session['email']
        else:
            print('current role is : ', request.session['role'])
            main_email = request.session['parent']
            # From post job form
        if request.method == "POST":
            try:
                # print('request for adding question')
                packageName = request.POST.get('packageName')
                question = request.POST.get('question')
                questionType = request.POST.get('questionType')

                doc_ref = db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document()
                db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document(doc_ref.id).set({
                    u'id': doc_ref.id,
                    u'question': question,
                    u'type': questionType,
                })
                return JsonResponse({"success": "true"})
            except:
                return JsonResponse({"success": "false"})


# except:
#     return HttpResponseRedirect('/')


def getPackages(request):
    try:
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Staff':
            if request.session['role'] == 'Recruiter':
                main_email = request.session['email']
            else:
                print('current role is : ', request.session['role'])
                main_email = request.session['parent']
                # From post job form
            if request.method == "GET":
                try:
                    # print('request for get user packages')
                    user_packages_docs = db.collection(u'users').document(main_email).collection(
                        u'packages').get()
                    user_packages = []
                    for doc in user_packages_docs:
                        # print(doc.id)
                        user_packages.append(doc.id)
                    return JsonResponse({"user_packages": user_packages})
                except:
                    return JsonResponse({"success": "false"})

    except:
        return HttpResponseRedirect('/')


def deletequestion(request):
    try:
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Staff':
            if request.session['role'] == 'Recruiter':
                main_email = request.session['email']
            else:
                print('current role is : ', request.session['role'])
                main_email = request.session['parent']
                # From post job form
            if request.method == "POST":
                try:
                    id = request.POST.get('id')
                    packageName = request.POST.get('packageName')
                    # print('deleting question with id=>', id, ' and package =>', packageName)
                    db.collection(u'users').document(main_email).collection(
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
        if request.session['role'] == 'Recruiter' or request.session['role'] == 'Librarian' or request.session[
            'role'] == 'Interviewer' or request.session['role'] == 'Staff':
            return render(request, 'recruiter/feedback.html', {'role': request.session['role'], 'name': request.session['name']})

    except:
        return HttpResponseRedirect('/')
