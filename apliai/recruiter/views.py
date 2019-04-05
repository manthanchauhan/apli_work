from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def dashboard(request):
    return render(request,'recruiter/dashboard.html')

    # return HttpResponse("Dashboard page working !")

def jobs(request):
    return render(request,'recruiter/jobs.html')

def candidates(request):
    return render(request,'recruiter/candidates.html')

def team(request):
    return render(request,'recruiter/teamhtml')

def question(request):
    return render(request,'recruiter/question.html')

def feedback(request):
    return render(request,'recruiter/feedback.html')