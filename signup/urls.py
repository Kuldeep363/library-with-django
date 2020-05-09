
from django.contrib import admin
from django.urls import path
from . import views as signup_view
urlpatterns = [
    path('',signup_view.signup,name='signup'),
]
 