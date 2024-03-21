from django.urls import path

from . import views

urlpatterns = [
    path("materias/<str:codigo>/<str:periodo>/crear-curso", views.crear_curso, name="crear-curso"),
    path("programas", views.programas, name="programas"),
    path("programas/<str:codigo>/<str:periodo>", views.programa, name="programa"),
    path("programas/<str:codigo>/<str:periodo>/editar-malla", views.malla_curricular, name="malla_curricular"),
    path("programas/<str:codigo>/<str:periodo>/guardar-malla", views.actualizar_malla, name="actualizar_malla_curricular"),
    path("cursos/<int:curso_id>/crear-clase", views.crear_clase, name="planeacion_materias"),
    path("visualizacion_clases/<str:nrc>/<str:id>", views.visualizacion_clase, name="visualizacion_clases"),
    path("materias/<str:codigo>/<str:periodo>", views.visualizacion_materia, name="visualizacion_materias"),
    path("materias", views.materias, name="materias"),

]
