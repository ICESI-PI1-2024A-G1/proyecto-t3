import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages import get_messages
from django.http import Http404, HttpRequest
from django.test import RequestFactory
from django.urls import reverse

from academico.models import (Director, EstadoSolicitud, Facultad, Programa,
                              TipoDePrograma)
from academico.views import programa
from usuarios.models import Ciudad


@pytest.fixture
def nuevo_programa():
    cali = Ciudad.objects.create(ciudad="Cali")
    facultadA = Facultad.objects.create(nombre="Facultad A")
    director = Director.objects.create(
        cedula="123456",
        nombre="juan",
        email="juan@gmail.com",
        telefono="123456",
        ciudad=cali,
        fechaNacimiento="2021-01-01",
        oficina="oficina",
    )
    aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
    maestria = TipoDePrograma.objects.create(nombre="Maestria")
    programa = Programa.objects.create(
        codigo="P1",
        nombre="Programa 1",
        facultad=facultadA,
        director=director,
        estado_solicitud=aprobado,
        tipo_de_programa=maestria,
    )
    return programa


@pytest.mark.django_db
def test_programa_view(nuevo_programa):
    request = RequestFactory().get(
        reverse("programa", args=[nuevo_programa.codigo, "2021-01"])
    )
    request.user = User.objects.create_user(username="admin", password="admin")

    response = programa(request, nuevo_programa.codigo, "2021-01")

    assert response.status_code == 200
    assert nuevo_programa.codigo.encode() in response.content
    assert nuevo_programa.nombre.encode() in response.content
    assert nuevo_programa.facultad.nombre.encode() in response.content
    assert nuevo_programa.director.nombre.encode() in response.content
    assert nuevo_programa.director.email.encode() in response.content
    assert nuevo_programa.director.telefono.encode() in response.content
    assert nuevo_programa.estado_solicitud.nombre.encode() in response.content
    assert b"11.500.000 $" in response.content


@pytest.mark.django_db
def test_programa_view_not_authenticated(nuevo_programa):
    factory = RequestFactory()
    request = factory.get(reverse("programa", args=[nuevo_programa.codigo, "202101"]))
    request.user = AnonymousUser()

    response = programa(request, nuevo_programa.codigo, "202101")

    assert response.status_code == 302
    assert response.url == "/login?next=" + reverse(
        "programa", args=[nuevo_programa.codigo, "202101"]
    )


@pytest.mark.django_db
def test_programa_view_invalid_programa(nuevo_programa):
    request = RequestFactory().get(reverse("programa", args=["P2", "2021-01"]))
    request.user = User.objects.create_user(username="admin", password="admin")

    try:
        programa(request, "P2", )
        assert False
    except Http404:
        assert True
