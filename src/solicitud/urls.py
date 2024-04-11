from django.urls import path

from . import views

urlpatterns = [
    path("crear_viatico", views.solicitud_viaticos, name="crear_viatico")
]