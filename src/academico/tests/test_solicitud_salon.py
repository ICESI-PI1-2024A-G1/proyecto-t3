import datetime
from django.http import QueryDict
from datetime import datetime, timedelta
from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import (EstadoSolicitud, Facultad, Programa,
                              TipoDePrograma)
from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from academico.views import programas, solicitar_salones
from usuarios.models import Ciudad, Director, Persona, Usuario
from solicitud.models import SolicitudEspacio, SolicitudClases


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
    grupo = mixer.blend('auth.Group', name='lideres')
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
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
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id = 1, periodo = periodo)
    return curso

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

@pytest.fixture
def estado_solicitud(db):
    """
    Esta función es un fixture que crea una instancia de EstadoSolicitud para ser utilizada en pruebas.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Una instancia de EstadoSolicitud creada con un estado de 1.
    """
    return EstadoSolicitud.objects.create(estado=1)
    
@pytest.fixture
def crear_instancias(db, curso):
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
    clase_1 = Clase.objects.create(fecha_inicio=datetime.now(), fecha_fin=datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    clase_2 = Clase.objects.create(fecha_inicio=datetime.now()+ timedelta(days=7), fecha_fin=datetime.now()+ timedelta(days=7), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    clase_3 = Clase.objects.create(fecha_inicio=datetime.now()+ timedelta(days=14), fecha_fin=datetime.now()+ timedelta(days=14), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    clases = [clase_1, clase_2, clase_3]
    return clases





@pytest.mark.django_db
def test_solicitar_salones_post_negativo_sin_clases(autenticacion, curso, estado_solicitud):
    """
    Prueba unitaria para verificar el comportamiento del método solicitar_salones al recibir una solicitud POST sin clases.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        curso: Objeto de curso para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = QueryDict('', mutable=True)
    request.POST.update = {
        'clases': []
    }
    response = solicitar_salones(request, curso.nrc)
    assert response.status_code == 302
    assert SolicitudEspacio.objects.count() == 1

@pytest.mark.django_db
def test_solicitar_salones_post_positivo_con_clases(autenticacion, curso, crear_instancias, estado_solicitud):
    """
    Prueba unitaria para verificar el comportamiento del método solicitar_salones al recibir una solicitud POST válida.

    Args:
        autenticacion: Objeto de autenticación para simular la autenticación del usuario.
        curso: Objeto de curso para utilizar en la prueba.
        crear_instancias: Lista de objetos de clase para utilizar en la prueba.

    Returns:
        None
    """
    request = autenticacion
    request.method = 'POST'
    request.POST = QueryDict('', mutable=True)
    request.POST.update = {
        'clases': [clase.id for clase in crear_instancias]
    }
    response = solicitar_salones(request, curso.nrc)
    assert response.status_code == 302
    assert SolicitudEspacio.objects.count() == 1
    #assert SolicitudClases.objects.count() == len(crear_instancias)