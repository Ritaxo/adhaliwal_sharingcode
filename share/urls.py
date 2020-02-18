from django.urls import path, include
from . import views #import evrything from module

app_name = "share"

urlpatterns =[path("", views.index, name= "index"),]
