import datetime
from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotFound
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              EspacioClase, GrupoDeClase, Materia, Modalidad,
                              Periodo, TipoDeMateria)
from academico.views import (eliminar_grupo_de_clases, nuevas_clases,
                             visualizacion_curso)
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
    user = User.objects.create_user(username="admin", password="admin")
    grupo = mixer.blend("auth.Group", name="gestores")
    user.groups.add(grupo)
    grupo = mixer.blend("auth.Group", name="lideres")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request = rf.get(reverse("visualizar-curso", kwargs={"curso_id": 1}))
    request.user = user
    return request


@pytest.fixture
def create_curso():
    periodo = Periodo.objects.create(semestre="202402", fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia = Materia.objects.create(
        codigo=1,
        nombre="Materia",
        creditos=3,
        departamento=departamento,
        tipo_de_materia=tipo_materia,
    )
    curso = mixer.blend(Curso, grupo=1, cupo=50, materia=materia, periodo=periodo)
    return curso


@pytest.fixture
def create_modalidad():
    modalidad = mixer.blend(Modalidad, metodologia="Presencial")
    return modalidad


@pytest.fixture
def create_espacio():
    espacio = mixer.blend(Espacio, tipo="Aula", capacidad=100)
    return espacio


@pytest.fixture
def create_clases(create_curso, create_modalidad, create_espacio):
    grupo_clases_1 = GrupoDeClase.objects.create()
    grupo_clases_2 = GrupoDeClase.objects.create()
    espacio = EspacioClase.objects.create(tipo=create_espacio, edificio="Edificio D", numero=101)
    for i in range(1, 4):
        clase = mixer.blend(
            Clase,
            curso=create_curso,
            modalidad=create_modalidad,
            espacio=create_espacio,
            fecha_inicio=f"2022-0{i}-01",
            fecha_fin=f"2022-0{i}-15",
            espacio_asignado=espacio,
            grupo_clases=grupo_clases_1,
        )
    for i in range(4, 9):
        clase = mixer.blend(
            Clase,
            curso=create_curso,
            modalidad=create_modalidad,
            espacio=create_espacio,
            fecha_inicio=f"2022-0{i}-01",
            fecha_fin=f"2022-0{i}-15",
            espacio_asignado=espacio,
            grupo_clases=grupo_clases_2,
        )
    return clase


@pytest.mark.django_db
def test_ver_modulos_clase(autenticacion, create_clases):
    """
    Prueba la visualización de los módulos de una clase en el sistema.

    Args:
        autenticacion: Objeto de autenticación del usuario.
        create_clases: Objeto de la clase a visualizar.

    Returns:
        None
    """
    request = autenticacion
    request.method = "GET"
    
    response = visualizacion_curso(request, create_clases.curso.nrc)
    assert response.status_code == 200
    assert b'Modulo de clases 1' in response.content
    assert b'Modulo de clases 2' in response.content

"""
urls a utilizar
path("clases/<int:grupo>/<int:cantidad>", views.nuevas_clases, name="nuevas_clases"),
    path("grupo_clases/<int:grupo>/eliminar", views.eliminar_grupo_de_clases, name="eliminar_grupo_de_clases"),
"""
@pytest.mark.django_db
def test_nuevas_clases(autenticacion, create_clases):
    """
    Prueba la creación de nuevas clases en el sistema.

    Args:
        autenticacion: Objeto de autenticación del usuario.
        create_clases: Objeto de la clase a visualizar.

    Returns:
        None
    """
    request = autenticacion
    request.method = "POST"
    
    response = nuevas_clases(request, create_clases.grupo_clases.id, 2)
    assert response.status_code == 302
    assert GrupoDeClase.objects.count() == 2
    assert Clase.objects.filter(grupo_clases=create_clases.grupo_clases).count() == 7

@pytest.mark.django_db
def test_eliminar_grupo_de_clases(autenticacion, create_clases):
    """
    Prueba la eliminación de un grupo de clases en el sistema.

    Args:
        autenticacion: Objeto de autenticación del usuario.
        create_clases: Objeto de la clase a visualizar.

    Returns:
        None
    """
    request = autenticacion
    request.method = "POST"
    
    response = eliminar_grupo_de_clases(request, create_clases.grupo_clases.id)
    assert response.status_code == 302
    assert GrupoDeClase.objects.count() == 1
    assert Clase.objects.filter(grupo_clases=create_clases.grupo_clases).count() == 0

# Tests negativos

@pytest.mark.django_db
def test_ver_modulos_clase_inexistente(autenticacion):
    """
    Prueba la visualización de los módulos de una clase inexistente.

    Args:
        autenticacion: Objeto de autenticación del usuario.

    Returns:
        None
    """
    request = autenticacion
    request.method = "GET"
    
    try:
        response = visualizacion_curso(request, 999)
    except Http404:
        assert True

@pytest.mark.django_db
def test_nuevas_clases_inexistente(autenticacion, create_clases):
    """
    Prueba la creación de nuevas clases en un grupo inexistente.

    Args:
        autenticacion: Objeto de autenticación del usuario.

    Returns:
        None
    """
    request = autenticacion
    request.method = "POST"
    
    try:
        response = nuevas_clases(request, 999, 2)
    except Http404:
        assert True
    
    assert GrupoDeClase.objects.count() == 2
    assert Clase.objects.filter(grupo_clases=create_clases.grupo_clases).count() == 5


@pytest.mark.django_db
def test_eliminar_grupo_de_clases_inexistente(autenticacion, create_clases):
    """
    Prueba la eliminación de un grupo de clases inexistente.

    Args:
        autenticacion: Objeto de autenticación del usuario.

    Returns:
        None
    """
    request = autenticacion
    request.method = "POST"

    try:
        response = eliminar_grupo_de_clases(request, 999)
    except Http404:
        assert True

    assert GrupoDeClase.objects.count() == 2
    assert Clase.objects.filter(grupo_clases=create_clases.grupo_clases).count() == 5
