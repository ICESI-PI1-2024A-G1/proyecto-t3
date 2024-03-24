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
    return RequestFactory()

@pytest.fixture
def autenticacion(db, rf):
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('crear-curso', kwargs={'codigo': '1', 'periodo': '202402'}))
    request.user = user
    return request

@pytest.fixture
def materia(db):
    return mixer.blend(Materia)

@pytest.fixture
def periodo_202402(db):
    return Periodo.objects.create(semestre='202402',fecha_inicio='2024-01-01',fecha_fin='2024-12-31')

@pytest.mark.django_db
def test_crear_curso_get(autenticacion, materia):
    response = crear_curso(autenticacion, materia.codigo, '202402')
    assert response.status_code == 200

@pytest.mark.django_db
def test_crear_curso_post_negativo(autenticacion, materia):
    request = autenticacion
    request.method = 'POST'
    request.POST = {
        'cantidad_de_cupos': 30
    }
    with pytest.raises(Http404):
        crear_curso(request, materia.codigo, '202402')

@pytest.mark.django_db
def test_crear_curso_post_positivo(autenticacion, materia, periodo_202402):
    request = autenticacion
    request.method = 'POST'
    request.POST = {
        'cantidad_de_cupos': 30
    }
    response = crear_curso(request, materia.codigo, '202402')
    assert response.status_code == 302
