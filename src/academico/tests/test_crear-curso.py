import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from mixer.backend.django import mixer
from academico.models import Curso, Periodo, Materia
from academico.views import crear_curso
from django.http import Http404


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
    Fixture for authentication.

    This fixture creates a user with the username 'admin' and password 'admin'.
    It also creates a request object with the URL for creating a course, passing
    the course code and period as kwargs. The user is then assigned to the request
    object. This fixture is used for testing the creation of a course.

    Args:
        db: Django test database fixture.
        rf: RequestFactory fixture.

    Returns:
        request: Request object with authenticated user.

    """
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('crear-curso', kwargs={'codigo': '1', 'periodo': '202402'}))
    request.user = user
    return request

@pytest.fixture
def materia(db):
    """
    Fixture function that creates and returns a blended Materia object.

    Parameters:
    - db: The database fixture.

    Returns:
    - A blended Materia object.
    """
    return mixer.blend(Materia)

@pytest.fixture
def periodo_202402(db):
    """
    Fixture function that creates a Periodo object with the specified attributes.

    Args:
        db: Django database fixture.

    Returns:
        Periodo: The created Periodo object.

    """
    return Periodo.objects.create(semestre='202402',fecha_inicio='2024-01-01',fecha_fin='2024-12-31')

@pytest.mark.django_db
def test_crear_curso_post_negativo(autenticacion, materia):
    """
    Test case for creating a course with a negative scenario.

    Args:
        autenticacion: The authentication object.
        materia: The materia object.

    Raises:
        Http404: If the course creation raises a Http404 exception.

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
    Test case for creating a course with a positive POST request.

    Args:
        autenticacion: The authentication object.
        materia: The materia object.
        periodo_202402: The periodo object.

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
