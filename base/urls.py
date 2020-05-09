from django.contrib import admin
from django.urls import path,re_path,include
from . import views as view
from signup import views as signView
urlpatterns = [
    path('',view.index,name='home'),
    path('sendMail',view.sendMail,name='mail'),
    path('dashboard',view.dashboard,name='dashboard'),
    path('logout',view.logoutUser,name='logout'),
     path('login',include('login.urls')),
    path('signup',include('signup.urls')),
    path('password-reset-request',signView.passResetRequest,name='resetPassword'),
    re_path(r'^resetPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',signView.reset_password, name='resetingPassword'), 
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',signView.activate, name='activate'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
  
