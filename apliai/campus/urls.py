from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('batch', views.batch, name="batch"),
    path('company', views.company, name="company"),
    path('analysis', views.analysis, name="analysis"),
    path('feedback', views.feedback, name="feedback"),
]