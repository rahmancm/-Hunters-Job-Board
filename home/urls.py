from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.loginUser,name='login'),
    path('logout',views.logoutUser,name='logout'),
    path('register',views.register,name='register'),
    path('postj',views.post,name='postj'),
    path('job_single/<int:pk>/',views.job_single,name='job_single'),
    path('profile',views.profile,name='profile')

]