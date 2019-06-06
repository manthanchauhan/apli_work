from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('jobs', views.jobs, name="jobs"),
    path('candidates', views.candidates, name="candidates"),
    path('team', views.team, name="team"),
    path('deleteteamuser', views.deleteteamuser, name="deleteteamuser"),
    path('inviteteamuser', views.inviteteamuser, name="inviteteamuser"),
    path('feedback', views.feedback, name="feedback"),
    path('question', views.question, name="question"),
    path('deletepost',views.deletepost,name="deletepost"),
    path('addpackage', views.addpackage, name="addpackage"),
    path('loadquestions', views.loadquestions, name="loadquestions"),
    path('addquestion', views.addquestion, name="addquestion"),
    path('deletequestion', views.deletequestion, name="deletequestion"),
    path('getPackages', views.getPackages, name="getPackages"),
    path('changepackage', views.changepackage, name="changepackage"),

]
