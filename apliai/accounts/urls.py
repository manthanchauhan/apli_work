from django.urls import path,include,re_path
from . import views

urlpatterns = [
    re_path(r'^reachus', views.reachus , name='reachus'),
    re_path(r'^login', views.login , name='login'),
    re_path(r'^signup', views.signup , name='signup'),
    re_path(r'^step1', views.step1 , name='step1'),
    re_path(r'^step2', views.step2 , name='step2'),
    re_path(r'^step3', views.step3 , name='step3'),    
    re_path(r'^logout', views.logout , name='logout'),        
]
