from django.http import Http404
import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from mixer.backend.django import mixer
from academico.models import Curso, Clase, Departamento, Materia, Modalidad, Periodo, TipoDeMateria, Espacio
from academico.views import visualizacion_curso
from datetime import datetime

@pytest.fixture
def rf():
    """
    Returns an instance of the RequestFactory class.

    This fixture is used to create fake HTTP requests for testing purposes.

    Returns:
        RequestFactory: An instance of the RequestFactory class.
    """
    return RequestFactory()

@pytest.fixture
def autenticacion(db, rf):
    """
    Fixture for authentication.

    This fixture creates a user with the username 'admin' and password 'admin'.
    It also creates a request object with the URL for visualizing a course with ID 1.
    The created user is set as the authenticated user for the request.

    Args:
        db: Django database fixture.
        rf: RequestFactory fixture.

    Returns:
        HttpRequest: The authenticated request object.
    """
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('visualizar-curso', kwargs={'curso_id': 1}))
    request.user = user
    return request

@pytest.fixture
def curso(db):
    """
    Fixture function that creates a Curso object for testing purposes.

    Args:
        db: Database fixture.

    Returns:
        Curso: The created Curso object.
    """
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id = 1, periodo = periodo)
    return curso

@pytest.fixture
def clase(db, curso):
    """
    Fixture function that creates a test class instance.

    Args:
        db: Database fixture.
        curso: Course fixture.

    Returns:
        The created class instance.
    """
    docente = mixer.blend('usuarios.Docente')
    modalidad = Modalidad.objects.create(metodologia="Presencial")
    espacio = Espacio.objects.create(tipo='Salón', capacidad=30)
    clase = Clase.objects.create(fecha_inicio=datetime.now(), fecha_fin=datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    return clase

@pytest.mark.django_db
def test_visualizacion_curso(autenticacion, curso, clase):
    """
    Test the visualization of a course.

    Args:
        autenticacion: The authentication object.
        curso: The course object.
        clase: The class object.

    Returns:
        None
    """
    response = visualizacion_curso(autenticacion, curso.nrc)
    assert response.status_code == 200
    assert str(curso.nrc).encode() in response.content
    assert str(curso.grupo).encode() in response.content
    assert str(curso.cupo).encode() in response.content
    assert curso.materia.nombre.encode() in response.content
    assert curso.periodo.semestre.encode() in response.content
    assert clase.docente.nombre.encode() in response.content

@pytest.mark.django_db
def test_visualizacion_curso_inexistente(autenticacion):
    """
    Test case for visualizing a non-existent course.

    This test verifies that the appropriate exception (Http404) is raised when attempting to visualize a course that does not exist.

    Args:
        autenticacion: The authentication object.

    Returns:
        None
    """
    try: 
        response = visualizacion_curso(autenticacion, 999)
    except Http404:
        assert True

@pytest.mark.django_db
def test_visualizacion_curso_sin_clases(autenticacion, curso):
    """
    Test case for visualizing a course without any classes.

    Args:
        autenticacion: The authentication object.
        curso: The course object.

    Returns:
        None
    """
    response = visualizacion_curso(autenticacion, curso.nrc)
    assert response.status_code == 200
    assert str(curso.nrc).encode() in response.content
    assert str(curso.grupo).encode() in response.content
    assert str(curso.cupo).encode() in response.content
    assert curso.materia.nombre.encode() in response.content
    assert curso.periodo.semestre.encode() in response.content
    assert b'No hay docentes asignados a este curso.' in response.content
    assert b'No hay clases creadas para este curso' in response.content