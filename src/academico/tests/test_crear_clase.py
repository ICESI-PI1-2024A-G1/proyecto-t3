import datetime
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotFound
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.test import TestCase, Client
from django.urls import reverse
from academico.models import Docente, Curso, Espacio, Modalidad, Clase, Periodo
from academico.views import crear_clase
import pytest
import pytest
from datetime import datetime


@pytest.fixture
def rf():
    """
    Returns an instance of the Django RequestFactory.
    This fixture is used to create mock request objects for testing purposes.
    """
    return RequestFactory()

@pytest.fixture
def autenticacion(db, rf):
    """
    Fixture que simula la autenticación de un usuario para visualizar un curso.

    Args:
        db: Objeto de la base de datos.
        rf: Objeto de la solicitud HTTP.

    Returns:
        request: Objeto de la solicitud HTTP con el usuario autenticado.
    """
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('planeacion_materias', kwargs={'curso_id': 1}))
    request.user = user
    return request

@pytest.fixture
def curso(db):
    """
    Fixture que crea y retorna un objeto de tipo Curso para ser utilizado en pruebas.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Curso: Objeto de tipo Curso creado para pruebas.
    """
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id = 1, periodo = periodo)
    return curso

@pytest.mark.django_db
def test_crear_clase_post_negativo_1(autenticacion):
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'espacio_id': '13',
       'modalidad_id': '4',
       'docente_id': '1000000000'
    }
    response = crear_clase(request, 2)
    assert isinstance(response, HttpResponseNotFound)

@pytest.mark.django_db
def test_crear_clase_post_negativo_01(autenticacion):
    # Crear un curso con un ID específico
    Curso.objects.create(nrc=1,grupo=7,cupo=30,materia_id=101,periodo_id=202401)

    # Configurar la solicitud
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'espacio_id': '13',
       'modalidad_id': '4',
       'docente_id': '1000000000'
    }

    # Llamar a la vista con un ID de curso que no existe
    response = crear_clase(request, 2)
    

    # Verificar que la respuesta es una instancia de HttpResponseNotFound
    assert isinstance(response, HttpResponseNotFound)


@pytest.mark.django_db
def test_crear_clase_post_negativo_2(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
       'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'curso_id': -1,
       'espacio_id': 12,
       'modalidad_id': 3,
       'docente_id': 1000000000

    }
    with pytest.raises(Http404):
        crear_clase(request, -1)


@pytest.mark.django_db
def test_crear_clase_post_negativo_3(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
       'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'curso_id': 3,
       'espacio_id': 12,
       'modalidad_id': 3,
       'docente_id': 1000000000

    }
    with pytest.raises(Http404):
        crear_clase(request, 3)

@pytest.mark.django_db
def test_crear_clase_post_negativo_4(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
       'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'curso_id': 0,
       'espacio_id': 12,
       'modalidad_id': 4,
       'docente_id': 1000000000

    }
    with pytest.raises(Http404):
        crear_clase(request, 0)
    
    
@pytest.mark.django_db
def test_crear_clase_post_positivo(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'curso_id': 1,
       'espacio_id': 12,
       'modalidad_id': 4,
       'docente_id': 3456789012
    }
    response = crear_clase(request, curso.nrc)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_crear_clase_post_positivo_docente_null(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': None,
       'curso_id': 1,
       'espacio_id': 12,
       'modalidad_id': 4,
       'docente_id': None
    }
    response = crear_clase(request, curso.nrc)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_crear_clase_post_positivo_espacio_null(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        'start_day': '2022-12-01T13:15',
       'end_day': '2022-12-01T15:15',
       'espacio_asignado': '205E',
       'curso_id': 1,
       'espacio_id': 12,
       'modalidad_id': 4,
       'docente_id': 2345678901
    }
    response = crear_clase(request, curso.nrc)
    assert response.status_code == 200
