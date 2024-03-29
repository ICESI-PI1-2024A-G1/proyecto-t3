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
    """
    Crea y devuelve un nuevo programa de prueba.

    Returns:
        Programa: El programa de prueba creado.
    """
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
    """
    Prueba la vista del programa.

    Esta función realiza pruebas para verificar el comportamiento de la vista del programa.
    Se asegura de que la vista responda correctamente y muestre la información correcta del programa.

    Args:
        nuevo_programa (Programa): El programa de prueba.

    Returns:
        None
    """
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
    """
    Prueba la vista del programa cuando el usuario no está autenticado.

    Args:
        nuevo_programa: Un objeto que representa un programa académico.

    Returns:
        None
    """
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
    """
    Prueba unitaria para verificar el comportamiento de la vista 'programa' cuando se proporciona un programa inválido.

    Se crea una solicitud HTTP utilizando la clase RequestFactory y se establece el usuario como un usuario creado previamente.
    Luego se llama a la vista 'programa' con un programa y un periodo académico inválidos.
    Se espera que se genere una excepción Http404, lo cual indica que no se encontró el recurso solicitado.

    Args:
        nuevo_programa: Un objeto que representa un programa académico creado previamente.

    Raises:
        AssertionError: Si la vista 'programa' no genera una excepción Http404.

    """
    request = RequestFactory().get(reverse("programa", args=["P2", "202101"]))
    request.user = User.objects.create_user(username="admin", password="admin")

    try:
        programa(request, "P2", "202101")
        assert False
    except Http404:
        assert True


@pytest.mark.django_db
def test_malla_curricular_empty_page(nuevo_programa):
    """
    Prueba unitaria para verificar que se muestra correctamente una página vacía de la malla curricular.

    Args:
        nuevo_programa (Programa): El programa académico para el cual se desea verificar la página vacía.

    Returns:
        None
    """
    request = RequestFactory().get(
        reverse("programa", args=[nuevo_programa.codigo, "2021-01"])
    )
    request.user = User.objects.create_user(username="admin", password="admin")

    response = programa(request, nuevo_programa.codigo, "2021-01")

    assert response.status_code == 200
    assert nuevo_programa.codigo.encode() in response.content
    assert nuevo_programa.nombre.encode() in response.content
    assert b"2021-01" in response.content
    assert b"No hay materias en esta malla curricular" in response.content
