from django.urls import path
from . import views as buy_view
from bookBank import views as bookBank_view
urlpatterns = [
    path('',bookBank_view.index,name='buyBooks')
]
