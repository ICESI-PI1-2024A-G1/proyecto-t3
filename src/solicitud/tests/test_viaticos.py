from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from mixer.backend.django import mixer

from academico.models import Clase, Curso
from solicitud.models import SolicitudViatico
from solicitud.views import viaticos
from usuarios.models import Persona, Usuario


def crear_instancias():
    curso= Curso.objects.create(nrc="1")
    clase1 = Clase.objects.create(id="100", curso=curso)
    clase2 = Clase.objects.create(id="101", curso=curso)
    clase3 = Clase.objects.create(id="102", curso=curso)
    SolicitudViatico.objects.create(descripcion="a", fecha_solicitud=datetime.now(), clase=clase1, tiquete=True, hospedaje=True, alimentacion=False)
    SolicitudViatico.objects.create(descripcion="a", fecha_solicitud=datetime.now(), clase=clase2, tiquete=True, hospedaje=True, alimentacion=True)
    SolicitudViatico.objects.create(descripcion="a", fecha_solicitud=datetime.now(), clase=clase3, tiquete=False, hospedaje=True, alimentacion=True)

def autenticar_usuario(request):
    """
    Autentica al usuario en la aplicación.

    Parámetros:
    - request: La solicitud HTTP recibida.

    Retorna:
    None
    """ 
    user = User.objects.create_user(username='admin', password='admin')
    grupo = mixer.blend("auth.Group", name="gestores")
    user.groups.add(grupo)
    persona = mixer.blend(Persona)
    mixer.blend(Usuario, persona=persona, usuario=user)
    request.user = user

@pytest.mark.django_db
def test_busqueda_clase_existe():
    """
    Prueba la búsqueda de una solicitud de viatico con una id de clase que existe dentro la lista de clases creada.

    Esta prueba verifica que la función `viaticos` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = '103'

    autenticar_usuario(request)
    response = viaticos(request)

    assert response.status_code == 200
    assert b'100' in response.content
