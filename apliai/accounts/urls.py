from django.urls import path, include, re_path
from . import views

app_name = 'accounts'
urlpatterns = [
    re_path(r'^reachus', views.reachus, name='reachus'),
    re_path(r'^login', views.login, name='login'),
    re_path(r'^signup', views.signup, name='signup'),
    re_path(r'^campus_signup', views.campus_signup, name='campus_signup'),
    re_path(r'^step1', views.step1, name='step1'),
    re_path(r'^step2', views.step2, name='step2'),
    re_path(r'^step3', views.step3, name='step3'),
    path('teamsignup/<encodeddata>/', views.teamsignup, name='teamsignup'),
    path('teamsignupcomplete/', views.teamsignupcomplete, name='teamsignupcomplete'),
    re_path(r'^logout', views.logout, name='logout'),
    re_path(r'^forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_confirm/<umail>/', views.reset_confirm, name='reset_confirm'),
    path('reset_password_successful', views.reset_password_successful, name='reset_password_successful')

]
