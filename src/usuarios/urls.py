from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_page, name="home"),
    path("login", views.login_page, name="login"),
    path("logout", views.log_out, name="logout"),
    path("docentes", views.docentes, name="docentes"),
    path("docentes/<str:cedula>/<str:periodo>", views.docente_Detail, name="ver_docente"),
    path("administrador", views.administrador, name="administrador"),
    path("administrador/<str:username>/change_state", views.change_state, name="change_state"),
    path("administrador/<str:username>/<str:rol>/change_rol", views.change_rol, name="change_rol"),
]
