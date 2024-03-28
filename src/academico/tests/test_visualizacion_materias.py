from django.http import Http404
import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from mixer.backend.django import mixer
from academico.models import Curso, Clase, Departamento, Materia, Modalidad, Periodo, TipoDeMateria, Espacio
from academico.views import visualizacion_materia
from datetime import datetime

pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def autenticacion(db, rf):
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('visualizacion_materias', kwargs={'codigo': 101, 'periodo': 202401} ))
    request.user = user
    return request

@pytest.fixture
def materias(db):
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    return materia

@pytest.fixture
def periodo(db):
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    return periodo

@pytest.mark.django_db
def test_visualizacion_materia(autenticacion, materia, periodo):
    response = visualizacion_materia(autenticacion, materia.codigo, periodo.semestre)
    assert response.status_code == 200
    assert str(materia.codigo).encode() in response.content
    assert str(materia.credito).encode() in response.content
    assert materia.nombre.encode() in response.content
    assert materia.departamento.nombre.encode() in response.content
    assert materia.tipo_materia.nombre.encode() in response.content

@pytest.mark.django_db
def test_visualizacion_materia_inexistente(autenticacion):
    try: 
        response = visualizacion_materia(autenticacion, 999, 0)
    except Http404:
        assert True
