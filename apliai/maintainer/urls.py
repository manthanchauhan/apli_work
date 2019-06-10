from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('users', views.users, name="users"),
    path('feedback', views.feedback, name="feedback"),
]