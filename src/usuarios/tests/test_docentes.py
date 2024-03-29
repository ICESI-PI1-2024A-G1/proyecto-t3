import pytest
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from usuarios.models import (Ciudad, Contrato, Director, Docente, EstadoContrato,
                     EstadoDocente, Persona, TipoContrato)
from usuarios.views import docentes

#SetUp de 3 docentes e la lista de docentes
def crear_instancias(): 
    fecha_elaboracion= "2023-01-01"
    tiempoCompleto = TipoContrato.objects.create(tipo= "Tiempo Completo")
    prestacionServicios = TipoContrato.objects.create(tipo= "Contrato de Prestación de Servicios")
    activoContrato= EstadoContrato.objects.create(estado =  "Activo")
    contrato1= Contrato.objects.create(codigo="1111", fecha_elaboracion=fecha_elaboracion, tipo_contrato= tiempoCompleto, estado_id=activoContrato.id)
    contrato2= Contrato.objects.create(codigo="2222", fecha_elaboracion=fecha_elaboracion, tipo_contrato= prestacionServicios, estado_id=activoContrato.id)
    contrato3 = Contrato.objects.create(codigo="3333", fecha_elaboracion=fecha_elaboracion, tipo_contrato= prestacionServicios, estado_id=activoContrato.id)
    activo = EstadoDocente.objects.create(estado = "Activo")
    inactivo = EstadoDocente.objects.create(estado = "Inactivo")
    medellin = Ciudad.objects.create(ciudad="Medellin")
    Docente.objects.create(cedula= "1104567892", nombre= "Daniel", email="dani@gmail.com", telefono="11222323", ciudad=medellin, fechaNacimiento="1989-04-03", contrato_codigo=contrato1, estado=activo)
    Docente.objects.create(cedula= "1123767462", nombre= "Esteban", email="esteban@gmail.com", telefono="11222323", ciudad=medellin, fechaNacimiento="1991-05-03", contrato_codigo=contrato2, estado=activo)
    Docente.objects.create(cedula= "9045678921", nombre= "Maria", email="maria@gmail.com", telefono="11222323", ciudad=medellin, fechaNacimiento="1988-06-03", contrato_codigo=contrato3, estado=inactivo)

def autenticar_usuario(request): 
    user = User.objects.create_user(username='admin', password='admin')
    request.user = user

@pytest.mark.django_db
def test_busqueda_docente_nombre_existe():
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = 'Daniel'

    #autenticar_usuario(request)
    response = docentes(request)

    assert response.status_code == 200
    assert b'Daniel' in response.content

@pytest.mark.django_db
def test_busqueda_docente_cedula_existe():
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = '9045678921'

    #autenticar_usuario(request)
    response = docentes(request)

    assert response.status_code == 200
    assert b'9045678921' in response.content

@pytest.mark.django_db
def test_busqueda_docente_nombre_Noexiste():
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = 'Camilo'

    #autenticar_usuario(request)
    response = docentes(request)

    assert response.status_code == 200
    assert b'Camilo' not in response.content

@pytest.mark.django_db
def test_filtrar_docente_por_estado():
    crear_instancias()
    request = RequestFactory().get('/?estado=1') #Se supone que la id=1 es la correspondiente a Activo

    response = docentes(request)
    assert response.status_code == 200
    assert b'Daniel' in response.content
    assert b'Esteban' in response.content
    assert b'Maria' not in response.content

@pytest.mark.django_db
def test_filtrar_docente_por_contrato():
    crear_instancias()
    request = RequestFactory().get('/?contrato=2') #Se supone que la id=2 es la correspondiente al tipo de contrato contrato de Prestación de servicios.

    response = docentes(request)
    assert response.status_code == 200
    assert b'Daniel' not in response.content
    assert b'Esteban' in response.content
    assert b'Maria' in response.content
    


