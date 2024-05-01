import json

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Espacio, EspacioClase,
                              EstadoSolicitud, GrupoDeClase, MallaCurricular,
                              Materia, Modalidad, Periodo, Programa)
from academico.views import enviar_para_aprobacion
from usuarios.models import Persona, Usuario


@pytest.fixture
def create_user():
    user = mixer.blend(User, username="testuser", password="testpassword")
    grupo = mixer.blend("auth.Group", name="lideres")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    return user

@pytest.fixture
def create_estado_solicitud():
    mixer.blend(EstadoSolicitud, nombre="Por aprobar")
    estado = mixer.blend(EstadoSolicitud, nombre="En proceso")
    return estado

@pytest.fixture
def create_periodo():
    periodo = mixer.blend(
        Periodo, semestre="2022-1", fecha_inicio="2022-01-01", fecha_fin="2022-01-15"
    )
    mixer.blend(
        Periodo, semestre="2022-2", fecha_inicio="2022-06-01", fecha_fin="2022-06-15"
    )
    return periodo


@pytest.fixture
def create_programa_academico(create_estado_solicitud):
    programa = mixer.blend(
        Programa,
        codigo="P001",
        nombre="Programa Académico 1",
        estado_solicitud=create_estado_solicitud,
    )
    return programa


@pytest.fixture
def create_materia():
    materia = mixer.blend(Materia, codigo=10, nombre="Materia 1")
    return materia


@pytest.fixture
def create_modalidad():
    modalidad = mixer.blend(Modalidad, metodologia="Presencial")
    return modalidad


@pytest.fixture
def create_espacio():
    espacio = mixer.blend(Espacio, tipo="Aula", capacidad=100)
    return espacio


@pytest.fixture
def create_malla(create_programa_academico, create_materia, create_periodo):
    malla = mixer.blend(
        MallaCurricular,
        programa=create_programa_academico,
        materia=create_materia,
        periodo=create_periodo,
    )
    return malla


@pytest.fixture
def create_curso(create_malla):
    curso = mixer.blend(
        Curso,
        grupo=1,
        cupo=50,
        materia=create_malla.materia,
        periodo=create_malla.periodo,
    )
    return curso


@pytest.fixture
def create_clases(create_curso, create_modalidad, create_espacio):
    grupo_clases = GrupoDeClase.objects.create()
    espacio = EspacioClase.objects.create(tipo=create_espacio, edificio="Edificio D", numero=101)
    for i in range(1, 9):
        clase = mixer.blend(
            Clase,
            curso=create_curso,
            modalidad=create_modalidad,
            espacio=create_espacio,
            fecha_inicio=f"2022-0{i}-01",
            fecha_fin=f"2022-0{i}-15",
            espacio_asignado=espacio,
            grupo_clases=grupo_clases,
        )
    return clase

@pytest.mark.django_db
def test_enviar_para_aprobacion_authenticated(create_user, create_clases):
    """
    Test case for the 'enviar_para_aprobacion' view function when the user is authenticated.

    This test verifies that the view function returns the expected response when a request is made
    with the necessary parameters and the user is authenticated.

    The test performs the following steps:
    1. Creates a request with the necessary parameters.
    2. Sets the user of the request to the created user.
    3. Calls the 'enviar_para_aprobacion' view function with the necessary parameters.
    4. Asserts that the response status code is 302.

    Args:
        create_user: A fixture that creates a user.
        create_programa_academico: A fixture that creates a program.
        create_periodo: A fixture that creates a period.

    Returns:
        None
    """
    # Create a request with the necessary parameters
    request = RequestFactory().post(
        reverse(
            "enviar_aprobacion",
            kwargs={"codigo": "P001", "periodo": "2022-1"},
        ),
        data=json.dumps({"comentarios": "Comentarios de prueba."}),
        content_type="application/json",
    )
    request.user = create_user

    # Call the view function
    response = enviar_para_aprobacion(request, "P001", "2022-1")

    assert response.status_code == 302
    assert Programa.objects.get(codigo="P001").estado_solicitud.nombre == "Por aprobar"

@pytest.mark.django_db
def test_enviar_para_aprobacion_unauthenticated(create_clases):
    """
    Test case for the 'enviar_para_aprobacion' view function when the user is unauthenticated.

    This test verifies that the view function returns the expected response when a request is made
    with the necessary parameters and the user is unauthenticated.

    The test performs the following steps:
    1. Creates a request with the necessary parameters.
    2. Calls the 'enviar_para_aprobacion' view function with the necessary parameters.
    3. Asserts that the response status code is 302.
    
    Args:
        create_programa_academico: A fixture that creates a program.
        create_periodo: A fixture that creates a period.

    Returns:
        None
    """
    # Create a request with the necessary parameters
    request = RequestFactory().post(
        reverse(
            "enviar_aprobacion",
            kwargs={"codigo": "P001", "periodo": "2022-1"},
        ),
        data=json.dumps({"comentarios": "Comentarios de prueba."}),
        content_type="application/json",
    )
    request.user = AnonymousUser()
    
    response = enviar_para_aprobacion(request, "P001", "2022-1")

    assert response.status_code == 302
    assert Programa.objects.get(codigo="P001").estado_solicitud.nombre == "En proceso"
