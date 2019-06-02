from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('jobs', views.jobs, name="jobs"),
    path('candidates', views.candidates, name="candidates"),
    path('team', views.team, name="team"),
    path('feedback', views.feedback, name="feedback"),
    path('question', views.question, name="question"),
    re_path(r'^addpackage', views.addpackage, name="addpackage"),
    re_path(r'^addquestion', views.addquestion, name="addquestion"),
    re_path(r'^deletequestion', views.deletequestion, name="deletequestion"),
    re_path(r'^changepackage', views.changepackage, name="changepackage"),

]
