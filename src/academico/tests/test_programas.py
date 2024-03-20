import pytest
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from academico.models import EstadoSolicitud, Facultad, Programa, TipoDePrograma
from usuarios.models import Ciudad, Director
from academico.views import programas

@pytest.mark.django_db
def test_busqueda_programa():
    # Creación de instancias de objetos necesarios
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

    # Creación de una solicitud GET con parámetros de búsqueda
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = 'Programa 1' 

    # Creación de un usuario y autenticación
    user = User.objects.create_user(username='admin', password='admin')
    request.user = user

    # Solicitud a la vista programas
    response = programas(request)

    # Verificación del código de estado de la respuesta
    assert response.status_code == 200

    # Verificación de que el programa esperado esté presente en la respuesta
    assert b'Programa 1' in response.content
