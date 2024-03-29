import pytest
from django.contrib.auth.models import User
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import Curso, Materia, Periodo
from academico.views import crear_curso


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
    Fixture que simula la autenticación de un usuario para realizar pruebas en la vista 'crear-curso'.

    Args:
        db: Objeto de la base de datos.
        rf: Objeto de la clase RequestFactory.

    Returns:
        request: Objeto de la clase HttpRequest con la autenticación del usuario.
    """
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('crear-curso', kwargs={'codigo': '1', 'periodo': '202402'}))
    request.user = user
    return request

@pytest.fixture
def materia(db):
    """
    Fixture que crea y retorna una instancia de la clase Materia.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Una instancia de la clase Materia.
    """
    return mixer.blend(Materia)

@pytest.fixture
def periodo_202402(db):
    """
    Crea y devuelve un objeto Periodo con los siguientes atributos:

    Args:
        db: Objeto de la base de datos.

    Returns:
        Un objeto Periodo con los siguientes atributos:
        - semestre: El semestre del periodo ('202402').
        - fecha_inicio: La fecha de inicio del periodo ('2024-01-01').
        - fecha_fin: La fecha de fin del periodo ('2024-12-31').
    """
    return Periodo.objects.create(semestre='202402', fecha_inicio='2024-01-01', fecha_fin='2024-12-31')

@pytest.mark.django_db
def test_crear_curso_post_negativo(autenticacion, materia):
    """
    Prueba la función crear_curso cuando se realiza una solicitud POST con una cantidad de cupos inválida.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        materia: Objeto de materia para simular la materia del curso.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
        'cantidad_de_cupos': 30
    }
    with pytest.raises(Http404):
        crear_curso(request, materia.codigo, '202402')

@pytest.mark.django_db
def test_crear_curso_post_positivo(autenticacion, materia, periodo_202402):
    """
    Prueba unitaria para verificar el comportamiento del método crear_curso al recibir una solicitud POST válida.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        materia: Objeto de materia para utilizar en la prueba.
        periodo_202402: Objeto de periodo para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
        'cantidad_de_cupos': 30
    }
    response = crear_curso(request, materia.codigo, '202402')
    assert response.status_code == 302
