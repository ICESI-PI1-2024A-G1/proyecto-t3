import pytest
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from academico.models import EstadoSolicitud, Facultad, Programa, TipoDePrograma
from usuarios.models import Ciudad, Director
from academico.views import programas

def crear_instancias():
    cali = Ciudad.objects.create(ciudad="Cali")
    facultadA = Facultad.objects.create(nombre="Facultad A")
    facultadB = Facultad.objects.create(nombre="Facultad B")
    director = Director.objects.create(cedula="123456", nombre="juan", email="juan@gmail.com", telefono="123456", ciudad=cali, fechaNacimiento="2021-01-01", oficina="oficina")
    aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
    pendiente = EstadoSolicitud.objects.create(nombre="Pendiente")
    rechazado = EstadoSolicitud.objects.create(nombre="Rechazado")
    maestria = TipoDePrograma.objects.create(nombre="Maestria")
    doctorado = TipoDePrograma.objects.create(nombre="Doctorado")
    Programa.objects.create(codigo="P1", nombre="Programa 1", facultad=facultadA, director=director, estado_solicitud=aprobado, tipo_de_programa=maestria)
    Programa.objects.create(codigo="P2", nombre="Programa 2", facultad=facultadB, director=director, estado_solicitud=pendiente, tipo_de_programa=doctorado)
    Programa.objects.create(codigo="P3", nombre="Programa 3", facultad=facultadA, director=director, estado_solicitud=rechazado, tipo_de_programa=maestria)

def autenticar_usuario(request):
    user = User.objects.create_user(username='admin', password='admin')
    request.user = user

@pytest.mark.django_db
def test_busqueda_programa():
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = 'Programa 1' 

    autenticar_usuario(request)

    response = programas(request)

    assert response.status_code == 200
    assert b'Programa 1' in response.content

@pytest.mark.django_db
def test_filtrar_programa_por_estado():
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['estado'] = '1'  # Suponiendo que el ID del estado "Aprobado" es 1

    autenticar_usuario(request) 

    response = programas(request)

    assert response.status_code == 200
    assert b'Programa 1' in response.content  # Suponiendo que el estado "Aprobado" está asociado al programa 1
    assert b'Programa 2' not in response.content  # Programa 2 no debería estar presente, ya que su estado no es "Aprobado"
    assert b'Programa 3' not in response.content  # Programa 3 no debería estar presente, ya que su estado no es "Aprobado"

@pytest.mark.django_db
def test_filtrar_programa_por_facultad():
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['facultad'] = '1'  # Suponiendo que el ID de la Facultad A es 1

    autenticar_usuario(request) 

    response = programas(request)

    assert response.status_code == 200
    assert b'Programa 1' in response.content  # Suponiendo que el programa 1 pertenece a la Facultad A
    assert b'Programa 2' not in response.content  # Programa 2 no debería estar presente, ya que no pertenece a la Facultad A
    assert b'Programa 3' in response.content  # Suponiendo que el programa 3 pertenece a la Facultad A
