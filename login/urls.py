
from django.contrib import admin
from django.urls import path,include
from . import views as login_view
urlpatterns = [
    path('',login_view.loginUser,name='login'),
    
]
 