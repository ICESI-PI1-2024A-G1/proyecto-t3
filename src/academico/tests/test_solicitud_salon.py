import datetime
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
    clase_2 = Clase.objects.create(fecha_inicio=datetime.now()+ datetime.timedelta(days=7), fecha_fin=datetime.now()+ datetime.timedelta(days=7), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    clase_3 = Clase.objects.create(fecha_inicio=datetime.now()+ datetime.timedelta(days=14), fecha_fin=datetime.now()+ datetime.timedelta(days=14), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    clases = list(clase_1, clase_2, clase_3)
    return clases


@pytest.mark.django_db
def test_solicitud_salones():
    curso = curso()
    clases = crear_instancias(curso)
    request = autenticacion
    request.method = 'POST'
    request.POST = {
        'clases': clases
    }
    
    response = solicitar_salones(request, curso)
    assert response.status_code == 200
    
    
    