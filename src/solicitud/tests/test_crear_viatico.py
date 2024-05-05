from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest, Http404
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from solicitud.models import SolicitudViatico
from academico.views import solicitar_viaticos, visualizacion_curso
from usuarios.models import Persona, Usuario, Docente

def crear_clases():
    """
    Crea instancias de objetos de tipo Clase en la base de datos para realizar pruebas.

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
        lista de clases creadas
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
    return [clase1, clase2]

def autenticar_usuario(request):
    """
    Autentica al usuario en la aplicación.

    Parámetros:
    - request: La solicitud HTTP recibida.

    Retorna:
    None
    """ 
    user = User.objects.create_user(username='admin', password='admin')
    grupo = mixer.blend("auth.Group", name="gestores")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user

@pytest.mark.django_db
def test_crear_viatico_post_positivo():
    """
    Prueba unitaria para verificar el comportamiento del método solicitar_viaticos al recibir una solicitud POST válida.

    Args:
        None

    Returns:
        None
    """
    clasesDisponibles=crear_clases()
    clase = clasesDisponibles[0]
    request = HttpRequest()

    autenticar_usuario(request)
    request.method = 'POST'
    request.POST = {
       'tiquetes':'on',
       'hospedaje':'on',
       'alimentacion':'on',
    }
   
    response = solicitar_viaticos(request,clase.id)
    assert response.status_code == 302
    assert SolicitudViatico.objects.count() == 1

@pytest.mark.django_db
def test_crear_viatico_post_positivo_sin_allitems():
    """
    Prueba unitaria para verificar el comportamiento del método solicitar_viaticos al recibir una solicitud POST válida pero sin hacer
    uso de todos los items.

    Args:
        None

    Returns:
        None
    """
    clasesDisponibles=crear_clases()
    clase = clasesDisponibles[1]
    request = HttpRequest()

    autenticar_usuario(request)
    request.method = 'POST'
    request.POST = {
       'tiquetes':'on',
       'hospedaje':'on',
       'alimentacion':'None',
    }
    response = solicitar_viaticos(request,clase.id)
    assert response.status_code == 302
    assert SolicitudViatico.objects.count() == 1

@pytest.mark.django_db
def test_crear_viatico_post_negativo_clase_inexistente():
    """
    Prueba unitaria para verificar el comportamiento del método solicitar_viaticos al realizar una solicitud POST de items válidos pero
    con una clase inexistente.

    Args:
        None

    Returns:
        None
    """
    request = HttpRequest()

    autenticar_usuario(request)
    request.method = 'POST'
    request.POST = {
       'tiquetes':'on',
       'hospedaje':'on',
       'alimentacion':'None',
    }
    try:
        response = solicitar_viaticos(request,999)
    except Http404:
        assert True
    assert SolicitudViatico.objects.count() == 0

@pytest.mark.django_db
def test_crear_viatico_post_negativo_sinItems():
    """
    Prueba unitaria para verificar el comportamiento del método solicitar_viaticos al realizar una solicitud POST donde
    no se requirió ningún item.

    Args:
        None

    Returns:
        None
    """
    clasesDisponibles=crear_clases()
    clase = clasesDisponibles[1]
    request = HttpRequest()

    autenticar_usuario(request)
    request.method = 'POST'
    request.POST = {
       'tiquetes':'None',
       'hospedaje':'None',
       'alimentacion':'None',
    }

    response = solicitar_viaticos(request,clase.id)
    assert response.status_code == 302
    assert SolicitudViatico.objects.count() == 0