from django.urls import path, include
from . import views  # import views module

app_name = 'share'

urlpatterns = [
    path('',views.index, name='index'),  # Module 0
    path('first_script', views.get_first_script, name='first_script'), # Module 1
]
