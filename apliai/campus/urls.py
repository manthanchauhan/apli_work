from django.urls import path
from . import views


urlpatterns = [
    path('cdashboard', views.cdashboard, name="cdashboard"),
    path('batch', views.batch, name="batch"),
    path('company', views.company, name="company"),
    path('analysis', views.analysis, name="analysis"),
    path('cfeedback', views.cfeedback, name="cfeedback"),
]