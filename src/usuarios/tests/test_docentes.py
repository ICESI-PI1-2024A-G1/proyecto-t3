import pytest
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from usuarios.models import (Ciudad, Contrato, Director, Docente, EstadoContrato,
                     EstadoDocente, Persona, TipoContrato)
from usuarios.views import docentes

#SetUp de 3 docentes e la lista de docentes
def crear_instancias():
    """
    Crea instancias de objetos en la base de datos para realizar pruebas.

    Esta función crea instancias de los siguientes objetos:
    - Ciudad
    - Contrato
    - TipoContrato
    - EstadoConrato
    - EstadoDocente
    - Docente

    Returns:
        None
    """ 
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
    """
    Autentica al usuario en la aplicación.

    Parámetros:
    - request: La solicitud HTTP recibida.

    Retorna:
    None
    """ 
    user = User.objects.create_user(username='admin', password='admin')
    request.user = user

@pytest.mark.django_db
def test_busqueda_docente_nombre_existe():
    """
    Prueba la búsqueda de un docente con un nombre de docente que existe dentro la lista de docentes creada.

    Esta prueba verifica que la función `docentes` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = 'Daniel'

    autenticar_usuario(request)
    response = docentes(request)

    assert response.status_code == 200
    assert b'Daniel' in response.content

@pytest.mark.django_db
def test_busqueda_docente_cedula_existe():
    """
    Prueba la búsqueda de un docente con una cedula de docente que existe dentro la lista de docentes creada.

    Esta prueba verifica que la función `docentes` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = HttpRequest()
    request.method = 'GET'
    request.GET['q'] = '9045678921'

    autenticar_usuario(request)
    response = docentes(request)

    assert response.status_code == 200
    assert b'9045678921' in response.content

@pytest.mark.django_db
def test_busqueda_docente_nombre_Noexiste():
    """
    Prueba la búsqueda de un docente con un nombre de docente que no exista dentro la lista de docentes creada.

    Esta prueba verifica que la función `docentes` responda correctamente a una solicitud GET con un parámetro
    de búsqueda y que devuelva un código de estado 200 junto con el contenido del programa buscado.

    Verificamos que la cedula a buscar no esté dentro del contenido arrojado por la lista al buscar.

    Args:
        None

    Returns:
        None
    """
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
    """
    Prueba unitaria para verificar el filtrado de programas por estado del docente.

    Se crean instancias de programas y se realiza una solicitud GET con el parámetro 'estado' establecido en '1',
    que supone que el ID del estado "Activo" es 1. Luego se autentica al usuario y se realiza la solicitud al
    controlador 'docentes'. Se verifica que la respuesta tenga un código de estado 200 y que el contenido de la
    respuesta contenga el docente Daniel y el docente Esteban, pero no la docente Maria, ya que su estado no es "Activo".

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = RequestFactory().get('/?estado=1') #Se supone que la id=1 es la correspondiente a Activo

    response = docentes(request)
    assert response.status_code == 200
    assert b'Daniel' in response.content
    assert b'Esteban' in response.content
    assert b'Maria' not in response.content

@pytest.mark.django_db
def test_filtrar_docente_por_contrato():
    """
    Prueba unitaria para verificar el filtrado de programas por tipo de contrato del docente.

    Se crean instancias de programas y se realiza una solicitud GET con el parámetro 'contrato' establecido en '2',
    que supone que el ID del Tipo de contrato "Contrato de Prestación de Servicios " es 2. Luego se autentica al usuario y se realiza la solicitud al
    controlador 'docentes'. Se verifica que la respuesta tenga un código de estado 200 y que el contenido de la
    respuesta contenga el docente Esteban y la docente Maria, pero no el docente Esteban, ya que su tipo de contrato no es "Contrato de Prestacion de Servicios".

    Args:
        None

    Returns:
        None
    """
    crear_instancias()
    request = RequestFactory().get('/?contrato=2') #Se supone que la id=2 es la correspondiente al tipo de contrato contrato de Prestación de servicios.

    response = docentes(request)
    assert response.status_code == 200
    assert b'Daniel' not in response.content
    assert b'Esteban' in response.content
    assert b'Maria' in response.content
    


