from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# General Stats
def mdashboard(request):
    name = request.session['name']
    email = request.session['email']
    return render(request,'maintainer/mdashboard.html',{'name':name})

# User management, Signup,remove,edit,etc on users db recruiter and campus
def users(request):
    return render(request,'maintainer/users.html')

# Feedback management, query handling both sides
def mfeedback(request):
    return render(request,'maintainer/mfeedback.html')
