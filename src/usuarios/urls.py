from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_page, name="login"),
    path("logout", views.log_out, name="logout"),
    path("ver_docente", views.docente_Detail, name="ver-docente")
]
