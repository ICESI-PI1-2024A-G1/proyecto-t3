from django.urls import path

from . import views

urlpatterns = [
    path("crear_viatico", views.solicitud_viaticos, name="crear_viatico"),
    path("salones_solicitud", views.salones_solicitud, name="salones_solicitud"),
    path("asignar_espacio/<int:solicitud_id>/", views.asignar_espacio, name="asignar_espacio"),
]