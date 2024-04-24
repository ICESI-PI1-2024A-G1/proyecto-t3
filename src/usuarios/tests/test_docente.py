from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Espacio,
                              EstadoSolicitud, Facultad, MallaCurricular,
                              Materia, Modalidad, Periodo, Programa,
                              TipoDeMateria)
from usuarios.models import (Ciudad, Contrato, Director, Docente,
                             EstadoContrato, EstadoDocente, Persona,
                             TipoContrato, Usuario)
from usuarios.views import docente_Detail


def autenticar_usuario(request):
    """
    Autentica al usuario en la aplicación.

    Args:
    - request: La solicitud HTTP recibida.

    Retorna:
    None
    """ 
    user = User.objects.create_user(username='admin', password='admin')
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user

@pytest.fixture
def docente(db):
    """
    Fixture que crea y devuelve un objeto de tipo Docente para usar en pruebas.

    Esta función crea instancias de los siguientes objetos:
    - Ciudad
    - Contrato
    - TipoContrato
    - EstadoConrato
    - EstadoDocente
    - Docente

    Args:
        db: Objeto de la base de datos.

    Returns:
        docente: Objeto de tipo Docente
    """ 
    fecha_elaboracion= "2023-01-01"
    tiempoCompleto = TipoContrato.objects.create(tipo= "Tiempo Completo")
    activoContrato= EstadoContrato.objects.create(estado =  "Activo")
    contrato1= Contrato.objects.create(codigo="1111", fecha_elaboracion=fecha_elaboracion, tipo_contrato= tiempoCompleto, estado_id=activoContrato.id)
    activo = EstadoDocente.objects.create(estado = "Activo")
    medellin = Ciudad.objects.create(ciudad="Medellin")
    docente = Docente.objects.create(cedula= "1104567892", nombre= "Daniel", email="dani@gmail.com", telefono="11222323", ciudad=medellin, fechaNacimiento="1989-04-03", contrato_codigo=contrato1, estado=activo)
    return docente


@pytest.fixture
def periodo(db):
    """
    Fixture que crea y devuelve un objeto de tipo Periodo para usar en pruebas.
    
    Args:
        db: Objeto de la base de datos.

    Returns:
        periodo: Objeto Periodo
    """
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    return periodo

@pytest.fixture
def curso(db, periodo):
    """
    Fixture que crea y retorna un objeto de tipo Curso para ser utilizado en pruebas.

    Args:
        db: Objeto de la base de datos.
        periodo: Objeto Periodo creado anteriormente

    Esta función crea instancias de los siguientes objetos:
    - Departamento
    - TipoDeMateria
    - Materia
    - Curso

    Returns:
        Curso: Objeto de tipo Curso creado para pruebas.
    """
    periodoN = periodo
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id = 1, periodo = periodoN)
    return curso

@pytest.fixture
def clase(db, curso, docente):
    """
    Esta función es un fixture que crea una instancia de la clase Clase para ser utilizada en pruebas.

    Args:
        db: Objeto de la base de datos.
        curso: Objeto del curso al que pertenece la clase.

    Returns:
        Una instancia de la clase Clase creada con los parámetros proporcionados.
    """
    docente = docente
    modalidad = Modalidad.objects.create(metodologia="Presencial")
    espacio = Espacio.objects.create(tipo='Salón', capacidad=30)
    clase = Clase.objects.create(fecha_inicio=datetime.now(), fecha_fin=datetime.now(), curso=curso, modalidad=modalidad, espacio=espacio, docente=docente)
    return clase
@pytest.mark.django_db
def test_visualizacion_docente_existe(docente, periodo):
    """
    Prueba que verifica la visualización de información de un docente existente.

    Args:
        docente: Fixture de objeto de Docente de prueba
        periodo: Fixture de objeto de Prueba

    Returns:
        None
    """
    request = HttpRequest()
    autenticar_usuario(request)
    response = docente_Detail(request, docente.cedula , periodo.semestre)
    fecha_nacimiento = datetime.strptime(docente.fechaNacimiento, '%Y-%m-%d')
    # Formatear la fecha de nacimiento al formato del HTML
    fecha_nacimiento_str = fecha_nacimiento.strftime('%b. %d, %Y')
    assert response.status_code == 200
    assert docente.cedula.encode() in response.content
    assert docente.nombre.encode() in response.content
    assert docente.telefono.encode() in response.content
    assert docente.email.encode() in response.content
    assert fecha_nacimiento_str.encode() 
    assert docente.contrato_codigo.tipo_contrato.tipo.encode() in response.content
    assert docente.estado.estado.encode() in response.content

@pytest.mark.django_db
def test_visualizacion_docente_inexistente():
    """
    Prueba que verifica la excepción Http404 cuando se intenta visualizar un docente inexistente.

    Returns:
        None
    """
    request = HttpRequest()
    autenticar_usuario(request)
    try: 
        response = docente_Detail(request, "11111", "202109")
    except Http404:
        assert True

@pytest.mark.django_db
def test_visualizacion_seccion_clase_vacia(docente, periodo):
    """
    Prueba que verifica la visualización de la seccion de clases de un docente, la cual está vacía.

    Args:
        docente: Fixture de objeto de Docente de prueba
        periodo: Fixture de objeto de Prueba

    Returns:
        None
    """
    request = HttpRequest()
    autenticar_usuario(request)
    response = docente_Detail(request, docente.cedula, "202101")

    assert response.status_code == 200
    assert docente.cedula.encode() in response.content
    assert docente.nombre.encode() in response.content
    assert b"202101" in response.content
    assert b"No hay clases programados para este periodo" in response.content

@pytest.mark.django_db
def test_visualizacion_seccion_una_clase(docente, periodo, clase):
    """
    Prueba que verifica la visualización de la seccion de clases de un docente, la cual contiene una clase.

    Args:
        docente: Fixture de objeto de Docente de prueba
        periodo: Fixture de objeto de Prueba
        clase: Fixture de objeto de Clase

    Returns:
        None
    """
    request = HttpRequest()
    autenticar_usuario(request)
    response = docente_Detail(request, docente.cedula, periodo.semestre)
    assert response.status_code == 200
    assert docente.cedula.encode() in response.content
    assert docente.nombre.encode() in response.content
    assert periodo.semestre.encode() in response.content
    assert clase.docente.cedula == docente.cedula
    assert clase.curso.grupo.encode() in response.content
