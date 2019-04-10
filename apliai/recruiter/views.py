from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def is_recruiter(self):
    print('in')
    if str(self.user_type) == 'Recruiter':
        print('here')
        return True
    else:
        return False
rec_login_required = user_passes_test(lambda u: True if u.is_recruiter else False, login_url='/')

def recruiter_login_required(view_func):
    decorated_view_func = login_required(rec_login_required(view_func), login_url='/')
    return decorated_view_func

@recruiter_login_required    
def dashboard(request):
    return render(request,'recruiter/dashboard.html')

def jobs(request):
    return render(request,'recruiter/jobs.html')

def postjob(request):
    if request.method == "POST":
        company_name = "Apli.ai"
        post = request.POST.get('post')
        job_description = request.POST.get('jobdesc')
        tskill = request.POST.get('tskill')
        sskill = request.POST.get('sskill')
        other = request.POST.get('other')
        bond = request.POST.get('bond')
        salary = request.POST.get('salary')
        add_detail = request.POST.get('adddetail')
    print(company_name,post,job_description,tskill,sskill,other,bond,salary,add_detail)
    return render(request,"recruiter/jobs.html")

def candidates(request):
    return render(request,'recruiter/candidates.html')

def team(request):
    return render(request,'recruiter/team.html')

def question(request):
    return render(request,'recruiter/question.html')

def feedback(request):
    return render(request,'recruiter/feedback.html')