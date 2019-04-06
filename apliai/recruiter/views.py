from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def dashboard(request):
    return render(request,'recruiter/dashboard.html')

    # return HttpResponse("Dashboard page working !")

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