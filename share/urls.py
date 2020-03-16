from django.urls import path, include
from . import views  # import views module

app_name = 'share'

urlpatterns = [
    path('',views.index, name='index'),  # Module 0
    path('first_script', views.get_first_script, name='first_script'), # Module 1
    # Module 3
    # authentication: signup, login, logout
    path('create', views.create, name='create'),
    path("loguser", views.login_user, name="loguser"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('publish_problem', views.publish_problem, name='publish_problem'),
    path('problem/<int:problem_id>/show', views.show_problem, name='show_problem'),
    # Module 4
path('problem/<int:problem_id>/show_my_problem', views.show_my_problem, name='show_my_problem'),

path('script/<int:script_id>/show_my_script', views.show_my_script, name='show_my_script'),



]
