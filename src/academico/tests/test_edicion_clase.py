import datetime
from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotFound
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from academico.views import editar_clase
from usuarios.models import Persona, Usuario


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
    grupo = mixer.blend("auth.Group", name="lideres")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
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
    curso = Curso.objects.create(grupo='4', cupo=30, materia_id=1, periodo=periodo)
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

@pytest.fixture
def docente(db):
    """
    Fixture que crea y retorna una instancia de la clase Docente.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Una instancia de la clase Docente.
    """
    return mixer.blend(Docente)

@pytest.fixture
def espacio(db):
    """
    Fixture que crea y retorna una instancia de la clase Espacio.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Una instancia de la clase Espacio.
    """
    return mixer.blend(Espacio)

@pytest.fixture
def modalidad(db):
    """
    Fixture que crea y retorna una instancia de la clase Modalidad.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Una instancia de la clase Modalidad.
    """
    return mixer.blend(Modalidad)

@pytest.mark.django_db
def test_editar_clase_post_negativo_clase_inexistente(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con una clase que no existe.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": clase.espacio.id,
        "modalidad_clase_e": clase.modalidad.id,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, 999)
        assert False
    except Http404 as e:
        assert True

@pytest.mark.django_db
def test_editar_clase_post_negativo_fecha_inicio_None(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con fecha de inicio None.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': None,
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": clase.espacio.id,
        "modalidad_clase_e": clase.modalidad.id,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Todos los campos son requeridos."

@pytest.mark.django_db
def test_editar_clase_post_negativo_fecha_fin_None(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con fecha de fin None.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': None,
       "espacio_asignado": None,
       "tipo_espacio_e": clase.espacio.id,
        "modalidad_clase_e": clase.modalidad.id,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Todos los campos son requeridos."

@pytest.mark.django_db
def test_editar_clase_post_negativo_tipo_espacio_None(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con tipo de espacio None.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": None,
        "modalidad_clase_e": clase.modalidad.id,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Todos los campos son requeridos."

@pytest.mark.django_db
def test_editar_clase_post_negativo_tipo_espacio_invalido(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con un tipo de espacio inválido.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": 100,
        "modalidad_clase_e": clase.modalidad.id,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Tipo de espacio no existe."

@pytest.mark.django_db
def test_editar_clase_post_negativo_modalidad_None(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con modalidad None.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": clase.espacio.id,
        "modalidad_clase_e": None,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Todos los campos son requeridos."

@pytest.mark.django_db
def test_editar_clase_post_negativo_modalidad_invalido(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con una modalidad inválida.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": clase.espacio.id,
        "modalidad_clase_e": 100,
        "docente_clase_e": clase.docente.cedula
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Modalidad no existe."

@pytest.mark.django_db
def test_editar_clase_post_negativo_docente_invalido(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST con un docente inválido.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       'espacio_asignado': None,
       'tipo_espacio_e': clase.espacio.id,
        'modalidad_clase_e': clase.modalidad.id,
        'docente_clase_e': 999
    }
    try:
        response = editar_clase(request, clase.id)
        assert False
    except Http404 as e:
        assert str(e) == "Docente no existe."

@pytest.mark.django_db
def test_editar_clase_post_positivo(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método editar_clase al recibir una solicitud POST válida.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = {
       'fecha_inicio': str(clase.fecha_inicio)[0:-10].replace(" ","T"),
       'fecha_fin': str(clase.fecha_fin)[0:-10].replace(" ","T"),
       "espacio_asignado": None,
       "tipo_espacio_e": clase.espacio.id,
        "modalidad_clase_e": clase.modalidad.id,
        "docente_clase_e": clase.docente.cedula
    }
    response = editar_clase(request, clase.id)
    assert response.status_code == 302
