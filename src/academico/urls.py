from django.urls import path

from . import views

urlpatterns = [
    path("crear-curso", views.crear_curso, name="crear-curso"),
    path("programas", views.programas, name="programas"),
    path("programa/<str:codigo>/<str:periodo>", views.programa, name="programa"),
    path("planeacion_materias", views.crear_clase, name="planeacion_materias"),
]
