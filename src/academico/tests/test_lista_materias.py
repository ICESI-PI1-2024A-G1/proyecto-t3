import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import Departamento, Materia, Programa, TipoDeMateria
from academico.views import materias
from usuarios.models import Persona, Usuario


def crear_instancias():
    """
    Creates instances of Departamento, TipoDeMateria, and Materia models for testing purposes.

    Returns:
        None
    """
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia1 = Materia.objects.create(codigo=1, nombre="Materia 1", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    materia2 = Materia.objects.create(codigo=2, nombre="Materia 2", creditos=4, departamento=departamento, tipo_de_materia=tipo_materia)

def autenticar_usuario(request):
    """
    Authenticates a user by creating a new user object with the username 'admin' and password 'admin',
    and assigns it to the request.user attribute.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        None
    """
    user = User.objects.create_user(username='admin', password='admin')
    grupo = mixer.blend("auth.Group", name="gestores")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user

@pytest.mark.django_db
def test_busqueda_materia():
    """
    Test case for searching a specific subject.

    This test case creates instances, authenticates a user, and sends a request to search for a subject.
    It then asserts that the response status code is 200 and that the content of the response contains 'Materia 1'.
    """
    crear_instancias()
    request = RequestFactory().get('/', {'q': 'Materia 1'})
    autenticar_usuario(request)
    response = materias(request)
    assert response.status_code == 200
    assert b'Materia 1' in response.content
