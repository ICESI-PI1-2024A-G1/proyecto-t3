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
                              Materia, Modalidad, Periodo, TipoDeMateria, GrupoDeClase)
from solicitud.models import SolicitudViatico
from solicitud.views import viaticos
from usuarios.models import Persona, Usuario, Docente


def crear_grupoDeClase():
    """
    Crea instancia de objeto tipo GrupoDeClase en la base de datos para realizar pruebas.

    Returns:
        El objeto GrupoDeClase creado
    """ 
    grupo_clase = GrupoDeClase.objects.create(id="1", entrega_notas=False)
    return grupo_clase

def crear_curso():
    """
    Crea instancia de objeto tipo Curso en la base de datos para realizar pruebas.

    Esta función crea instancias de los siguientes objetos:
    - Materia
    - Periodo

    Returns:
        El objeto Curso creado
    """
    materia = mixer.blend('academico.Materia')
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    curso= Curso.objects.create(nrc="1", grupo="1", cupo="30", materia=materia, periodo=periodo, intu_generado=True)
    return curso

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
def test_editar_entrego_notas():
    """
    Prueba unitaria para verificar el comportamiento del método change_notas de un grupo de clases existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    grupo_de_clase = crear_grupoDeClase()
    curso = crear_curso()
    response = client.post(reverse('change_notas', args=[curso.nrc, grupo_de_clase.id]))
    grupo_de_clase.refresh_from_db()
    assert response.status_code == 302
    assert grupo_de_clase.entrega_notas == True

@pytest.mark.django_db
def test_editar_intu_curso():
    """
    Prueba unitaria para verificar el comportamiento del método change_intu de un curso existente.
    Args:
        None

    Returns:
        None
    """

    request = HttpRequest()
    client = autenticar_usuario(request)
    curso = crear_curso()
    response = client.post(reverse('change_intu', args=[curso.nrc]))
    curso.refresh_from_db()
    assert response.status_code == 302
    assert curso.intu_generado == False