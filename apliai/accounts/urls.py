from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.login , name='login'),
    path('signup', views.signup , name='signup'),
    path('step1', views.step1 , name='step1'),
    path('step2', views.step2 , name='step2'),
    path('step3', views.step3 , name='step3'),    
    path('logout', views.logout , name='logout'),        
]
