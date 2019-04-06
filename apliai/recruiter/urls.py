from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard', views.dashboard , name="dashboard"),
    path('jobs', views.jobs , name="jobs"),
    path('postjob', views.postjob , name="postjob"),
    path('candidates', views.candidates , name="candidates"),
    path('team', views.candidates , name="team"),
    path('feedback', views.candidates , name="feedback"),
    path('question', views.candidates , name="question"),        
]
