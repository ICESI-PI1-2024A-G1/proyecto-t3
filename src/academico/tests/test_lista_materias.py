from django.http import HttpRequest
from django.test import RequestFactory
from django.contrib.auth.models import User

import pytest
from academico.models import Materia, TipoDeMateria, Departamento, Programa
from academico.views import materias

def crear_instancias():
    departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
    tipo_materia = TipoDeMateria.objects.create(tipo="1")
    materia1 = Materia.objects.create(codigo=1, nombre="Materia 1", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
    materia2 = Materia.objects.create(codigo=2, nombre="Materia 2", creditos=4, departamento=departamento, tipo_de_materia=tipo_materia)

def autenticar_usuario(request):
    user = User.objects.create_user(username='admin', password='admin')
    request.user = user

@pytest.mark.django_db
def test_busqueda_materia():
    crear_instancias()
    request = RequestFactory().get('/', {'q': 'Materia 1'})
    autenticar_usuario(request)
    response = materias(request)
    assert response.status_code == 200
    assert b'Materia 1' in response.content
