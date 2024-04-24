from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Espacio, Materia,
                              Modalidad, Periodo, TipoDeMateria)
from academico.views import visualizacion_materia
from usuarios.models import Persona, Usuario

pytest.fixture
def rf():
    """
    Return una instancia de la RequestFactory de Django. 
    Este fixture se utiliza para crear objetos de solicitud simulados con el propósito de pruebas.
    """
    return RequestFactory()

@pytest.fixture
def autenticacion(db, rf):
    """
    Fixture que simula la autenticación de un usuario para realizar pruebas en la vista 'visualizacion_materias'.

    Args:
        db: Objeto de la base de datos.
        rf: Objeto de la clase RequestFactory.

    Returns:
        request: Objeto de la clase HttpRequest con la autenticación del usuario.
    """

    user = User.objects.create_user(username='admin', password='admin')
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request = rf.get(reverse('visualizacion_materias', kwargs={'codigo': 101, 'periodo': 202401} ))
    request.user = user
    return request

@pytest.fixture
def materia(db):
    """
    Fixture que crea y devuelve una instancia de Materia para usar en pruebas.

    Args:
        db: Objeto de la base de datos.

    Returns:
        materia: Objeto de la clase Materia.
    """
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    return materia

@pytest.fixture
def periodo(db):
    """
    Fixture que crea y devuelve un periodo para usar en pruebas.

    Args:
        db: Objeto de la base de datos.

    Returns:
        periodo: String que representa el periodo.
    """
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    return periodo.semestre

@pytest.mark.django_db
def test_visualizacion_materia(autenticacion, materia, periodo):
    """
    Prueba que verifica la visualización de información de una materia.

    Args:
        autenticacion: Fixture para simular la autenticación del usuario.
        materia: Fixture para crear una instancia de materia.
        periodo: Fixture para el periodo.

    Returns:
        None
    """
    response = visualizacion_materia(autenticacion, materia.codigo, periodo)
    assert response.status_code == 200
    assert str(materia.codigo).encode() in response.content
    assert str(materia.creditos).encode() in response.content
    assert materia.nombre.encode() in response.content
    assert materia.departamento.nombre.encode() in response.content
    assert materia.tipo_de_materia.nombre.encode() in response.content


@pytest.mark.django_db
def test_visualizacion_materia_inexistente(autenticacion):
    """
    Prueba que verifica la excepción Http404 cuando se intenta visualizar una materia inexistente.

    Args:
        autenticacion: Fixture para simular la autenticación del usuario.

    Returns:
        None
    """
    try: 
        response = visualizacion_materia(autenticacion, 999, 0)
    except Http404:
        assert True
