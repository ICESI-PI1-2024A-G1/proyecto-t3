import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import (EstadoSolicitud, Facultad, Programa,
                              TipoDePrograma)
from academico.views import programas
from usuarios.models import Ciudad, Director, Persona, Usuario


def crear_instancias():
    """
    Crea instancias de objetos en la base de datos para realizar pruebas.

    Esta función crea instancias de los siguientes objetos:
    - Ciudad
    - Facultad
    - Director
    - EstadoSolicitud
    - TipoDePrograma
    - Programa

    Returns:
        None
    """
    cali = Ciudad.objects.create(ciudad="Cali")
    facultadA = Facultad.objects.create(nombre="Facultad A")
    facultadB = Facultad.objects.create(nombre="Facultad B")
    director = Director.objects.create(cedula="123456", nombre="juan", email="juan@gmail.com", telefono="123456", ciudad=cali, fechaNacimiento="2021-01-01", oficina="oficina")
    aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
    pendiente = EstadoSolicitud.objects.create(nombre="Pendiente")
    rechazado = EstadoSolicitud.objects.create(nombre="Rechazado")
    maestria = TipoDePrograma.objects.create(nombre="Maestria")
    doctorado = TipoDePrograma.objects.create(nombre="Doctorado")
    Programa.objects.create(codigo="P1", nombre="Programa 1", facultad=facultadA, director=director, estado_solicitud=aprobado, tipo_de_programa=maestria)
    Programa.objects.create(codigo="P2", nombre="Programa 2", facultad=facultadB, director=director, estado_solicitud=pendiente, tipo_de_programa=doctorado)
    Programa.objects.create(codigo="P3", nombre="Programa 3", facultad=facultadA, director=director, estado_solicitud=rechazado, tipo_de_programa=maestria)

def autenticar_usuario(request):
    """
    Autentica al usuario en la aplicación.

    Parámetros:
    - request: La solicitud HTTP recibida.

    Retorna:
    None
    """
    user = User.objects.create_user(username='admin', password='admin')
    grupo = mixer.blend("auth.Group", name="lideres")
    user.groups.add(grupo)
    grupo = mixer.blend("auth.Group", name="gestores")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user

@pytest.mark.django_db
def test_busqueda_programa():
    """
    Prueba la búsqueda de un programa.

    Esta prueba verifica que la función `programas` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = 'Programa 1'
    autenticar_usuario(request)

    response = programas(request)

    assert response.status_code == 200
    assert b'Programa 1' in response.content

@pytest.mark.django_db
def test_filtrar_programa_por_estado():
    """
    Prueba unitaria para verificar el filtrado de programas por estado.

    Se crean instancias de programas y se realiza una solicitud GET con el parámetro 'estado' establecido en '1',
    que supone que el ID del estado "Aprobado" es 1. Luego se autentica al usuario y se realiza la solicitud al
    controlador 'programas'. Se verifica que la respuesta tenga un código de estado 200 y que el contenido de la
    respuesta contenga el programa 1, pero no el programa 2 ni el programa 3, ya que su estado no es "Aprobado".

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['estado'] = '1'  # Suponiendo que el ID del estado "Aprobado" es 1

    autenticar_usuario(request)

    response = programas(request)

    assert response.status_code == 200
    assert b'Programa 1' in response.content  # Suponiendo que el estado "Aprobado" está asociado al programa 1
    assert b'Programa 2' not in response.content  # Programa 2 no debería estar presente, ya que su estado no es "Aprobado"
    assert b'Programa 3' not in response.content  # Programa 3 no debería estar presente, ya que su estado no es "Aprobado"

@pytest.mark.django_db
def test_filtrar_programa_por_facultad():
    """
    Prueba la funcionalidad de filtrar programas por facultad.

    Args:
        Ninguno

    Returns:
        Ninguno
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['facultad'] = '1'  # Suponiendo que el ID de la Facultad A es 1

    autenticar_usuario(request) 

    response = programas(request)

    assert response.status_code == 200
    assert b'Programa 1' in response.content  # Suponiendo que el programa 1 pertenece a la Facultad A
    assert b'Programa 2' not in response.content  # Programa 2 no debería estar presente, ya que no pertenece a la Facultad A
    assert b'Programa 3' in response.content  # Suponiendo que el programa 3 pertenece a la Facultad A
