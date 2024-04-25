import pytest
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import (Departamento, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Periodo, Programa,
                              TipoDeMateria, TipoDePrograma)
from academico.views import malla_curricular
from usuarios.models import Ciudad, Director, Persona, Usuario


def crear_instancias():
    """
    Crea instancias de objetos relacionados para realizar pruebas.

    Esta función crea instancias de los siguientes objetos:
    - Ciudad
    - Facultad
    - Director
    - EstadoSolicitud
    - TipoDePrograma
    - Programa
    - Periodo
    - Departamento
    - TipoDeMateria
    - Materia
    - MallaCurricular

    Returns:
        None
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
    periodo = Periodo.objects.create(semestre="202101", fecha_inicio="2021-01-01", fecha_fin="2021-06-30")
    departamento = Departamento.objects.create(codigo="D1", nombre="Departamento 1")
    tipo_de_materia = TipoDeMateria.objects.create(nombre="Tipo 1")
    
    #For para crear 20 materias y agregarlas a la malla curricular
    for i in range(20):
        materia = Materia.objects.create(
            codigo=i,
            nombre=f"Materia {i}",
            creditos=3,
            departamento=departamento,
            tipo_de_materia=tipo_de_materia,
        )
        MallaCurricular.objects.create(programa=programa, periodo=periodo, semestre=1,  materia=materia)

def autenticar_usuario(request):
    """
    Autentica al usuario en la solicitud.

    Args:
    - request: La solicitud HTTP recibida.

    Returns:
    None
    """
    user = User.objects.create_user(username='admin', password='admin')
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user

@pytest.mark.django_db
def test_malla_curricular():
    """
    Prueba unitaria para verificar el funcionamiento de la vista 'malla_curricular'.

    Esta prueba verifica que la vista 'malla_curricular' responda correctamente
    a una solicitud GET con los parámetros 'codigo' y 'periodo' especificados.
    Se asegura que la respuesta tenga un código de estado 200, y que contenga
    la cadena 'Malla curricular', el periodo y las materias especificadas.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['codigo'] = 'P1'
    request.GET['periodo'] = '202101'

    autenticar_usuario(request)

    response = malla_curricular(request, codigo='P1', periodo='202101')

    assert response.status_code == 200
    assert b'Malla curricular' in response.content
    assert b'202101' in response.content
    assert b'Materia 1' in response.content
    assert b'Materia 2' in response.content
    assert b'Materia 3' in response.content
    assert b'Materia 4' in response.content
    

@pytest.mark.django_db
def test_malla_curricular_pagination():
    """
    Prueba la paginación de la malla curricular.

    Esta función crea instancias necesarias para la prueba, configura una petición 
    HTTP GET con parámetros específicos y autentica al usuario. Luego realiza una
    llamada a la vista 'malla_curricular' con los parámetros de código y periodo
    proporcionados en la petición. Finalmente, realiza una serie de aserciones para
    verificar que la respuesta de la vista es correcta.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['codigo'] = 'P1'
    request.GET['periodo'] = '202101'
    request.GET['page'] = '2'

    autenticar_usuario(request)

    response = malla_curricular(request, codigo='P1', periodo='202101')

    assert response.status_code == 200
    assert b'Malla curricular' in response.content
    assert b'202101' in response.content
    assert b'2 de' in response.content

@pytest.mark.django_db
def test_malla_curricular_empty_page():
    """
    Prueba unitaria para verificar el comportamiento de la vista 'malla_curricular' cuando no hay materias en la malla curricular.

    Se crean instancias necesarias para la prueba y se realiza una solicitud GET a la vista 'malla_curricular' con un código de programa y periodo específicos.
    Se autentica al usuario en la solicitud y se verifica que la respuesta tenga un código de estado 200.
    Además, se verifica que la respuesta contenga el texto 'Malla curricular', el periodo y el mensaje 'No hay materias en esta malla curricular'.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['codigo'] = 'P1'
    request.GET['periodo'] = '202102'
    request.GET['page'] = '10'

    autenticar_usuario(request)

    response = malla_curricular(request, codigo='P1', periodo='202102')

    assert response.status_code == 200
    assert b'Malla curricular' in response.content
    assert b'202102' in response.content
    assert b'No hay materias en esta malla curricular' in response.content
