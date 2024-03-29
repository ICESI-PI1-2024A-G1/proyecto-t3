from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Espacio, Materia,
                              Modalidad, Periodo, TipoDeMateria)
from academico.views import visualizacion_curso


@pytest.fixture
def rf():
    """
    Crea y devuelve una instancia de RequestFactory.

    Returns:
        RequestFactory: Una instancia de RequestFactory.
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
    request = rf.get(reverse('visualizar-curso', kwargs={'curso_id': 1}))
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
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id = 1, periodo = periodo)
    return curso

@pytest.fixture
def clase(db, curso):
    """
    Esta función es un fixture que crea una instancia de la clase Clase para ser utilizada en pruebas.

    Args:
        db: Objeto de la base de datos.
        curso: Objeto del curso al que pertenece la clase.

    Returns:
        Una instancia de la clase Clase creada con los parámetros proporcionados.
    """
    docente = mixer.blend('usuarios.Docente')
    modalidad = Modalidad.objects.create(metodologia="Presencial")
    espacio = Espacio.objects.create(tipo='Salón', capacidad=30)
    clase = Clase.objects.create(fecha_inicio=datetime.now(), fecha_fin=datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    return clase

@pytest.mark.django_db
def test_visualizacion_curso(autenticacion, curso, clase):
    """
    Prueba la visualización de un curso en el sistema.

    Args:
        autenticacion (objeto): Objeto de autenticación del usuario.
        curso (objeto): Objeto del curso a visualizar.
        clase (objeto): Objeto de la clase asociada al curso.

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
    Prueba la visualización de un curso inexistente.

    Args:
        autenticacion: Objeto de autenticación.

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
    Prueba la visualización de un curso sin clases.

    Args:
        autenticacion: Objeto de autenticación.
        curso: Objeto de curso.

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