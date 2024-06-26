from django.urls import path

from . import views



urlpatterns = [
    path("materias/<str:codigo>/<str:periodo>/crear-curso", views.crear_curso, name="crear-curso"),
    path("cursos/<int:curso_id>", views.visualizacion_curso, name="visualizar-curso"),
    path("cursos/<int:curso_id>/<int:grupoId>/change_notas", views.change_notas, name="change_notas"),
    path("cursos/<int:curso_id>/change_intu", views.change_intu, name="change_intu"),
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
    path("clases/<int:clase_id>/solicitar_viatico", views.solicitar_viaticos, name="solicitar_viaticos"),
    path("clases/<int:clase_id>/eliminar_viatico", views.eliminar_viatico, name="eliminar_viatico"),
    path("clases/<int:clase_id>/editar_tiquete", views.editar_tiquete, name="editar_tiquete"),
    path("clases/<int:clase_id>/editar_hospedaje", views.editar_hospedaje, name="editar_hospedaje"),
    path("clases/<int:clase_id>/editar_alimentacion", views.editar_alimentacion, name="editar_alimentacion"),
    path("clases/<int:grupo>/<int:cantidad>", views.nuevas_clases, name="nuevas_clases"),
    path("grupo_clases/<int:grupo>/eliminar", views.eliminar_grupo_de_clases, name="eliminar_grupo_de_clases"),
    #path("cursos/<int:curso_id>/clases/<int:clase_id>/editar_clase", views.editar_clase, name="editar_clase"),
    path('programas/<str:codigo_programa>/<str:periodo>/export/pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('programas/<str:codigo_programa>/<str:periodo>/export/excel/', views.export_to_excel, name='export_to_excel'),
    path("clases/<int:clase_id>/eliminar", views.eliminar_clase, name='eliminar_clase'),
    path("clases/<int:clase_id>/editar_clase", views.editar_clase, name="editar_clase"),
    path("inicio", views.inicio, name="inicio"),
    path("cursos/<int:curso_id>/solicitar_salones", views.solicitar_salones, name="solicitar_salones"),
    path("solicitud/salones_solicitud", views.solicitudes_salones, name="salones_solicitud"),
]
