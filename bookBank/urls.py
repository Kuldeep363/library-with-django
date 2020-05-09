from django.contrib import admin
from django.urls import path
from . import views as bank_views


urlpatterns = [
    path('',bank_views.index,name='bookBank'),
    path('subject/<slug:slug>',bank_views.subject,name='subject'),
    path('detail/<slug:slug>',bank_views.details,name='details'),
    path('authors/<slug:slug>',bank_views.author,name='author'),
    path('add-book',bank_views.addBook,name='addBook'), 
    path('edit-book/<slug:slug>',bank_views.editBook,name='editBook'),
    path('delete/<slug:slug>',bank_views.delete,name='delete'),
    path('download/<slug:slug>',bank_views.download_book,name='download')
]  

 