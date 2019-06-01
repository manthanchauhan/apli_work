from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard', views.dashboard , name="dashboard"),
    path('jobs', views.jobs , name="jobs"),
    path('candidates', views.candidates , name="candidates"),
    path('team', views.team , name="team"),
    path('feedback', views.feedback , name="feedback"),
    path('question', views.question , name="question"),

]
