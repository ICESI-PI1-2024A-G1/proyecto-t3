from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_page, name="home"),
    path("login", views.login_page, name="login"),
    path("logout", views.log_out, name="logout"),
    path("ver-docente/<str:cedula>", views.docente_Detail, name="ver-docente")
]
