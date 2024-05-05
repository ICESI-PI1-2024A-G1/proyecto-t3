from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from solicitud.models import SolicitudViatico
from solicitud.views import viaticos
from usuarios.models import Persona, Usuario, Docente

# SetUp de 3 viaticos en la lista de viaticos
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
        None
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
    clase3 = Clase.objects.create(id="102", fecha_inicio= datetime.now(), fecha_fin= datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente, grupo_clases=grupo_clases)
    SolicitudViatico.objects.create(descripcion="a", fecha_solicitud="2023-01-01", clase=clase1, tiquete=True, hospedaje=True, alimentacion=False)
    SolicitudViatico.objects.create(descripcion="a", fecha_solicitud=datetime.now(), clase=clase2, tiquete=True, hospedaje=False, alimentacion=True)
    SolicitudViatico.objects.create(descripcion="a", fecha_solicitud=datetime.now(), clase=clase3, tiquete=False, hospedaje=True, alimentacion=True)

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
def test_busqueda_viatico_existe():
    """
    Prueba la búsqueda de una solicitud de viatico con una id de clase que existe dentro la lista de viaticos creada.

    Esta prueba verifica que la función `viaticos` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.

    Args:
        None

    Returns:
        None
    """
    crear_viaticos()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = '103'

    autenticar_usuario(request)
    response = viaticos(request)

    assert response.status_code == 200
    assert b'100' in response.content

@pytest.mark.django_db
def test_filtrar_viaticos_por_hospedaje():
    """
    Prueba unitaria para verificar el filtrado de viaticos por estado del hospedaje.

    Se crean instancias de viaticos y se realiza una solicitud GET con el parámetro 'hospedaje' establecido en 'True'. 
    Luego se autentica al usuario y se realiza la solicitud al controlador 'viaticos'. Se verifica que la respuesta tenga 
    un código de estado 200 y que el contenido de la respuesta contenga los viaticos con los id de las clases asociadas 100 y 102, respectivamente, 
    pero no el viatico con el id de clase 101 asociado, ya que su estado es 'False'.

    Args:
        None

    Returns:
        None
    """
    crear_viaticos()
    request = RequestFactory().get('/?hospedaje=True')
    autenticar_usuario(request)

    response = viaticos(request)
    assert response.status_code == 200
    assert b'100' in response.content
    assert b'102' in response.content
    assert b'101' not in response.content

@pytest.mark.django_db
def test_filtrar_viaticos_por_tiquetes():
    """
    Prueba unitaria para verificar el filtrado de viaticos por estado del tiquete.

    Se crean instancias de viaticos y se realiza una solicitud GET con el parámetro 'tiquete' establecido en 'True'. 
    Luego se autentica al usuario y se realiza la solicitud al controlador 'viaticos'. Se verifica que la respuesta tenga 
    un código de estado 200 y que el contenido de la respuesta contenga los viaticos con los id de las clases asociadas 100 y 101, respectivamente, 
    pero no el viatico con el id de clase 102 asociado, ya que su estado es 'False'.

    Args:
        None

    Returns:
        None
    """
    crear_viaticos()
    request = RequestFactory().get('/?tiquete=True') #Se supone que la id=1 es la correspondiente a Activo
    autenticar_usuario(request)

    response = viaticos(request)
    assert response.status_code == 200
    assert b'100' in response.content
    assert b'101' in response.content
    assert b'102' not in response.content

@pytest.mark.django_db
def test_filtrar_viaticos_por_alimentacion():
    """
    Prueba unitaria para verificar el filtrado de viaticos por estado del alimentacion.

    Se crean instancias de viaticos y se realiza una solicitud GET con el parámetro 'alimentacion' establecido en 'False'. 
    Luego se autentica al usuario y se realiza la solicitud al controlador 'viaticos'. Se verifica que la respuesta tenga 
    un código de estado 200 y que el contenido de la respuesta contenga el viatico con el id de las clase 100 asociada, 
    pero no los viaticos con los id de clases 101 y 102, pues ambos su valor es 'True'.

    Args:
        None

    Returns:
        None
    """
    crear_viaticos()
    request = RequestFactory().get('/?alimentacion=False') #Se supone que la id=1 es la correspondiente a Activo
    autenticar_usuario(request)

    response = viaticos(request)
    assert response.status_code == 200
    assert b'101' not in response.content
    assert b'102' not in response.content
    assert b'100' in response.content

@pytest.mark.django_db
def test_busqueda_viatico_por_fecha():
    """
    Prueba la búsqueda de una solicitud de viatico con una fecha de clase que existe dentro la lista de viaticos creada.

    Esta prueba verifica que la función `viaticos` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.
    Se verifica que el contenido de la respuesta contenga el viatico con el id de las clase 100 asociada, 
    pero no los viaticos con los id de clases 101 y 102, pues el único viático con fecha de solicitud "2023-01-01" es la 100.

    Args:
        None

    Returns:
        None
    """
    crear_viaticos()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q2'] = "2023-01-01"

    autenticar_usuario(request)
    response = viaticos(request)

    assert response.status_code == 200
    assert b'100' in response.content
    assert b'101' not in response.content
    assert b'102' not in response.content