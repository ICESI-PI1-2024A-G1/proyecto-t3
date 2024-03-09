from django.urls import path

from . import views

urlpatterns = [
    path("crear-curso", views.crear_curso, name="crear-curso"),
    path("programas", views.programas, name="programas")
]