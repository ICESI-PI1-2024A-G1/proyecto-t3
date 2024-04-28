from django.urls import path

from . import views
urlpatterns = [
    path("viaticos", views.viaticos, name="viaticos")
]