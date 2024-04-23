import json

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Espacio, EspacioClase,
                              GrupoDeClase, MallaCurricular, Materia,
                              Modalidad, Periodo, Programa)
from academico.views import importar_malla, primera_clase_programa
from usuarios.models import Persona, Usuario


@pytest.fixture
def create_user():
    user = mixer.blend(User, username="testuser", password="testpassword")
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    return user


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
def create_programa_academico():
    programa = mixer.blend(Programa, codigo="P001", nombre="Programa Académico 1")
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
def test_primera_clase_programa_authenticated(create_user, create_clases):
    """
    Test case for the 'primera_clase_programa' view function when the user is authenticated.

    This test verifies that the view function returns the expected response when a request is made
    with the necessary parameters and the user is authenticated.

    The test performs the following steps:
    1. Creates a request with the necessary parameters.
    2. Sets the user of the request to the created user.
    3. Calls the 'primera_clase_programa' view function with the necessary parameters.
    4. Asserts that the response status code is 200.
    5. Asserts that the response content contains specific strings.

    This test assumes the existence of the 'primera_clase_programa' view function and the 'create_user'
    and 'create_clases' fixtures.

    Args:
        create_user: A fixture that creates a user.
        create_clases: A fixture that creates classes.

    Returns:
        None
    """
    # Create a request with the necessary parameters
    request = RequestFactory().get(
        reverse("primera-clase", kwargs={"codigo": "P001", "periodo": "2022-1"})
    )
    request.user = create_user

    # Call the view function
    response = primera_clase_programa(request, "P001", "2022-1")

    assert response.status_code == 200
    assert b"Materia 1" in response.content
    assert b"2022-01-01" in response.content
    assert b"2022-01-15" in response.content
    assert b"Aula" in response.content
    assert b"Presencial" in response.content
    assert b"8" in response.content


@pytest.mark.django_db
def test_primera_clase_programa_no_clases(
    create_user, create_programa_academico, create_materia, create_curso
):
    """
    Test case for the 'primera_clase_programa' view when there are no classes in the program.

    This test checks if the view returns a response with a status code of 200 and the expected content.

    Args:
        create_user: A fixture to create a user object.
        create_programa_academico: A fixture to create a program object.
        create_materia: A fixture to create a subject object.
        create_curso: A fixture to create a course object.
    """

    # Create a request with the necessary parameters
    request = RequestFactory().get(
        reverse("primera-clase", kwargs={"codigo": "P001", "periodo": "2022-1"})
    )
    request.user = create_user

    # Call the view function
    response = primera_clase_programa(request, "P001", "2022-1")

    # Check the response status code
    assert response.status_code == 200

    # Check the response content
    assert b'"total_clases": 0' in response.content


@pytest.mark.django_db
def test_importar_malla(create_user, create_clases):
    """
    Test case for importing a curriculum grid.

    This test case verifies the functionality of importing a curriculum grid
    by sending a POST request to the 'importar_malla' view with the necessary
    parameters. It checks the response status code, content, and the changes
    made to the database.

    Args:
        create_user: A fixture that creates a user for testing.
        create_clases: A fixture that creates classes for testing.
    """
    request_data = {
        "primera_clase_actual": "2022-01-15",
        "primera_clase_importar": "2022-01-15T00:00:00Z",
        "incluir_docentes": True,
        "periodo_importar": "P001/2022-1",
    }
    json_data = json.dumps(request_data)
    # Create a request with the necessary parameters
    request = RequestFactory().post(
        reverse(
            "importar_malla",
            kwargs={"codigo": "P001", "periodo": "2022-2"},
        ),
        data=json_data,
        content_type="application/json",
    )
    request.user = create_user
    request.method = "POST"

    # Call the view function
    assert Clase.objects.all().count() == 8
    response = importar_malla(request, "P001", "2022-2")

    # Check the response status code
    assert response.status_code == 200

    # Check the response content
    assert b"success" in response.content
    assert Clase.objects.all().count() == 16
    assert MallaCurricular.objects.all().count() == 2
    assert Curso.objects.filter(periodo__semestre="2022-2").count() == 1


@pytest.mark.django_db
def test_importar_malla_inexistente(create_user, create_clases):
    """
    Test case for importing a non-existent curriculum.

    This test case checks the behavior of the importar_malla view function when
    attempting to import a curriculum that does not exist. It verifies that the
    response status code is 200 and that the number of Clase, MallaCurricular,
    and Curso objects remain unchanged.

    Args:
        create_user: A fixture that creates a user for testing purposes.
        create_clases: A fixture that creates a set of classes for testing purposes.
    """

    request_data = {
        "primera_clase_actual": "2022-01-15",
        "primera_clase_importar": "2022-01-15T00:00:00Z",
        "incluir_docentes": True,
        "periodo_importar": "P001/2022-0",
    }
    json_data = json.dumps(request_data)
    # Create a request with the necessary parameters
    request = RequestFactory().post(
        reverse(
            "importar_malla",
            kwargs={"codigo": "P001", "periodo": "2022-2"},
        ),
        data=json_data,
        content_type="application/json",
    )
    request.user = create_user
    request.method = "POST"

    # Call the view function
    assert Clase.objects.all().count() == 8
    response = importar_malla(request, "P001", "2022-2")

    # Check the response status code
    assert response.status_code == 200

    assert Clase.objects.all().count() == 8
    assert MallaCurricular.objects.all().count() == 1
    assert Curso.objects.filter(periodo__semestre="2022-2").count() == 0
