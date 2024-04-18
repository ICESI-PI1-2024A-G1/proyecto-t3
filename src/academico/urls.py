from django.urls import path

from . import views

urlpatterns = [
    path("materias/<str:codigo>/<str:periodo>/crear-curso", views.crear_curso, name="crear-curso"),
    path("cursos/<int:curso_id>", views.visualizacion_curso, name="visualizar-curso"),
    path("programas", views.programas, name="programas"),
    path("programas/<str:codigo>/<str:periodo>", views.programa, name="programa"),
    path("programas/<str:codigo>/<str:periodo>/obtener-primera-clase", views.primera_clase_programa, name="primera-clase"),
    path("programas/<str:codigo>/<str:periodo>/importar", views.importar_malla, name="importar_malla"),
    path("programas/<str:codigo>/<str:periodo>/editar-malla", views.malla_curricular, name="malla_curricular"),
    path("programas/<str:codigo>/<str:periodo>/guardar-malla", views.actualizar_malla, name="actualizar_malla_curricular"),
    path("programas/<str:codigo>/<str:periodo>/enviar-aprobacion", views.enviar_para_aprobacion, name="enviar_aprobacion"),
    path("cursos/<int:curso_id>/crear-clase", views.crear_clase, name="planeacion_materias"),
    path("materias/<str:codigo>/<str:periodo>", views.visualizacion_materia, name="visualizacion_materias"),
    path("materias", views.materias, name="materias"),
    #path("cursos/<int:curso_id>/editar_clase", views.editar_clase, name="editar_clase"),
    path("clases/<int:clase_id>", views.editar_clase, name="editar_clase"),
    #path("cursos/<int:curso_id>/clases/<int:clase_id>/editar_clase", views.editar_clase, name="editar_clase"),
    path('programas/<str:codigo_programa>/<str:periodo>/export/pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('programas/<str:codigo_programa>/<str:periodo>/export/excel/', views.export_to_excel, name='export_to_excel'),
    path("clases/<int:clase_id>/eliminar", views.eliminar_clase, name='eliminar_clase'),
    path("inicio", views.inicio, name="inicio"),
]
