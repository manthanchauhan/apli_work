from django.urls import path
from . import views


urlpatterns = [
    path('mdashboard', views.mdashboard, name="mdashboard"),
    path('users', views.users, name="users"),
    path('mfeedback', views.mfeedback, name="mfeedback"),
]