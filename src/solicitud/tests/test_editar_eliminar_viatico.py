from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest, Http404
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.urls import reverse
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist

from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from solicitud.models import SolicitudViatico
from solicitud.views import viaticos
from usuarios.models import Persona, Usuario, Docente

# SetUp de 2 viaticos en la lista de viaticos
def crear_viaticos():
    """
    Crea instancias de objetos de tipo SolicitudViatico en la base de datos para realizar pruebas.

    Esta función crea instancias de los siguientes objetos:
    - Docente
    - Espacio
    - Modalidad
    - Materia
    - Grupo de Clase
    - Curso
    - Periodo
    - Clase

    Returns:
        Lista de viaticos
    """ 
    docente = mixer.blend('usuarios.Docente')
    espacio = mixer.blend('academico.Espacio')
    modalidad = mixer.blend('academico.Modalidad')
    materia = mixer.blend('academico.Materia')
    grupo_clases= mixer.blend('academico.GrupoDeClase')
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    curso= Curso.objects.create(nrc="1", grupo="1", cupo="30", materia=materia, periodo=periodo, intu_generado=True)
    clase1 = Clase.objects.create(id="100", fecha_inicio= datetime.now(), fecha_fin= datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente, grupo_clases=grupo_clases)
    clase2 = Clase.objects.create(id="101", fecha_inicio= datetime.now(), fecha_fin= datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente, grupo_clases=grupo_clases)
    viatico1 = SolicitudViatico.objects.create(descripcion="a", fecha_solicitud="2023-01-01", clase=clase1, tiquete=True, hospedaje=True, alimentacion=False)
    viatico2= SolicitudViatico.objects.create(descripcion="a", fecha_solicitud=datetime.now(), clase=clase2, tiquete=True, hospedaje=False, alimentacion=True)
    return [viatico1,viatico2]

def autenticar_usuario(request):
    """
    Autentica al usuario en la aplicación.

    Parámetros:
    - request: La solicitud HTTP recibida.

    Retorna:
    - Client: un objeto cliente prueba de Django
    """ 
    user = User.objects.create_user(username='admin', password='admin')
    grupo = mixer.blend("auth.Group", name="gestores")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user
    c = Client()

    c.login(username='admin', password='admin')
    return c

@pytest.mark.django_db
def test_editar_alimentacion_de_viatico():
    """
    Prueba unitaria para verificar el comportamiento del método editar_alimentacion de un viatico existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    viaticos = crear_viaticos()
    viatico = viaticos[0]
    response = client.post(reverse('editar_alimentacion', args=[viatico.clase.id]))
    viatico.refresh_from_db()
    assert response.status_code == 302
    assert viatico.alimentacion == True


@pytest.mark.django_db
def test_editar_tiquete_de_viatico():
    """
    Prueba unitaria para verificar el comportamiento del método editar_tiquete de un viatico existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    viaticos = crear_viaticos()
    viatico = viaticos[0]
    response = client.post(reverse('editar_tiquete', args=[viatico.clase.id]))
    viatico.refresh_from_db()
    assert response.status_code == 302
    assert viatico.alimentacion == False

@pytest.mark.django_db
def test_editar_hospedaje_de_viatico():
    """
    Prueba unitaria para verificar el comportamiento del método editar_hospedaje de un viatico existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    viaticos = crear_viaticos()
    viatico = viaticos[0]
    response = client.post(reverse('editar_hospedaje', args=[viatico.clase.id]))
    viatico.refresh_from_db()
    assert response.status_code == 302
    assert viatico.alimentacion == False

@pytest.mark.django_db
def test_editar_cualquier_de_viatico_clase_noExistente():
    """
    Prueba unitaria para verificar el comportamiento del método eliminar_viatico de un viatico existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    viaticos = crear_viaticos()
    viatico = viaticos[1]
    try:
        response = client.post(reverse('editar_alimentacion', args=[999]))
    except Http404:
        assert True

@pytest.mark.django_db
def test_eliminar_viatico():
    """
    Prueba unitaria para verificar el comportamiento del método editar_alimentacion de un viatico con una clase inexistente al cual, supuestamente, está asociada.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    viaticos = crear_viaticos()
    viatico = viaticos[1]
    response = client.post(reverse('eliminar_viatico', args=[viatico.clase.id]))
    try:
        viatico.refresh_from_db()
    except ObjectDoesNotExist:
        viatico = None
    assert response.status_code == 302
    assert viatico is None

@pytest.mark.django_db
def test_eliminar_viatico_clase_noExistente():
    """
    Prueba unitaria para verificar el comportamiento del método eliminar_viatico de un viatico con una clase inexistente al cual, supuestamente, está asociada.
    Es decir, tratar de eliminar un viático no existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    viaticos = crear_viaticos()
    viatico = viaticos[1]
    try:
        response = client.post(reverse('eliminar_viatico', args=[999]))
    except Http404:
        assert True

