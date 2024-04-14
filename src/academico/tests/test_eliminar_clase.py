import datetime
from datetime import datetime

from django.shortcuts import get_object_or_404
import pytest
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotFound
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from academico.views import editar_clase
from academico.views import eliminar_clase


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
def test_eliminar_clase(rf, curso, clase, autenticacion):
    """
    Esta función de prueba verifica que una clase sea eliminada correctamente.

    Args:
        rf: Objeto de la solicitud HTTP.
        curso: Objeto del curso al que pertenece la clase.
        clase: Objeto de la clase a eliminar.
        autenticacion: Objeto de la solicitud HTTP con el usuario autenticado.

    Returns:
        None
    """
    request = rf.get(reverse('eliminar_clase', kwargs={'clase_id': clase.id}))
    request.user = autenticacion.user
    response = editar_clase(request, clase.id)
    assert response.status_code == 302
    assert Clase.objects.count() == 1


@pytest.mark.django_db
def test_eliminar_clase_post_negativo_clase_inexistente(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método eliminar_clase al recibir una solicitud POST con una clase que no existe.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    try:
        response = eliminar_clase(request, 999)
        assert False
    except Http404 as e:
        assert True


@pytest.mark.django_db
def test_eliminar_clase_post_positivo_clase_existente(autenticacion, clase):
    """
    Prueba unitaria para verificar el comportamiento del método eliminar_clase al recibir una solicitud POST con una clase que existe.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        clase: Objeto de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    try:
        response = eliminar_clase(request, clase.id)
        assert response.status_code == 302  # Verifica que la respuesta sea una redirección
        with pytest.raises(Http404):
            get_object_or_404(Clase, id=clase.id)  # Verifica que la clase ya no exista
    except Http404 as e:
        assert False