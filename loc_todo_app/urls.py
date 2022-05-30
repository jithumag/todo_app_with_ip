from django.urls import path

from .views import (home, register,log_in,log_out,update_todo, complete_todo,
    delete_todo)


urlpatterns = [
    path("", home, name="home"),
    path("login/",log_in,name="login"),
    path("logout/",log_out,name="logout"),
    path("register/", register, name="register"),
    path("update/todo/<int:pk>/", update_todo, name="update_todo"),
    path("complete/todo/<int:pk>/", complete_todo, name="complete_todo"),
    path("delete/todo/<int:pk>/", delete_todo, name="delete_todo"),
]