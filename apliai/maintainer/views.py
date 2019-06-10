from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# General Stats
def dashboard(request):
    name = request.session['name']
    email = request.session['email']
    return render(request,'maintainer/dashboard.html')

# User management, Signup,remove,edit,etc on users db recruiter and campus
def users(request):
    return render(request,'maintainer/users.html')

# Feedback management, query handling both sides
def feedback(request):
    return render(request,'maintainer/feedback.html')
