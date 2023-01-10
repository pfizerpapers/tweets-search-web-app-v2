from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('executafuncao', views.executafuncao, name='executafuncao'),
    path('tweetscount', views.tweetscount, name='tweetscount'),
]