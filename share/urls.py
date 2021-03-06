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
    path('dashboard', views.dashboard, name='dashboard'),
    path('publish/problem', views.publish_problem, name='publish_problem'),
    path("problem/create", views.create_problem, name="create_problem"),
    path('problem/<int:problem_id>/show', views.show_problem, name='show_problem'),

    # Module 4

path("problem/<int:problem_id>/build_script", views.build_script, name = 'build_script'),
path("problem/<int:problem_id>/create_script", views.create_script, name = 'create_script'),
path('script/<int:script_id>/show', views.show_script, name='show_script'),
path('problem/<int:problem_id>/edit', views.edit_problem,  name='edit_problem'),
path('script/<int:script_id>/edit', views.edit_script, name='edit_script'),
path('problem/<int:problem_id>/update', views.update_problem, name='update_problem'),
path('script/<int:script_id>/update', views.update_script, name='update_script'),
path('problem/<int:problem_id>/delete', views.delete_problem, name='delete_problem'),
path('script/<int:script_id>/delete', views.delete_script, name='delete_script'),
path('script/<int:script_id>/create_review', views.create_review, name='create_review'),
path('review/<int:review_id>/delete_review', views.delete_review, name='delete_review'),
path('search', views.search, name='search'),

]
