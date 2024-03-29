import pytest
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from academico.models import EstadoSolicitud, Facultad, Programa, TipoDePrograma
from usuarios.models import Ciudad, Director
from academico.views import programas

def crear_instancias():
    """
    Creates instances of various models for testing purposes.

    This function creates instances of the following models:
    - Ciudad
    - Facultad
    - Director
    - EstadoSolicitud
    - TipoDePrograma
    - Programa

    Returns:
    None
    """
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
    """
    Authenticates a user by creating a new user with the username 'admin' and password 'admin',
    and assigns it to the request object.

    Args:
        request (HttpRequest): The request object.

    Returns:
        None
    """
    user = User.objects.create_user(username='admin', password='admin')
    request.user = user

@pytest.mark.django_db
def test_busqueda_programa():
    """
    Test case for searching a program.

    This test case verifies that the 'programas' view returns a response with status code 200
    and the content contains the program name 'Programa 1'.

    Steps:
    1. Create necessary instances.
    2. Create a GET request with a search query for 'Programa 1'.
    3. Authenticate the user.
    4. Call the 'programas' view with the request.
    5. Assert that the response status code is 200.
    6. Assert that the response content contains the program name 'Programa 1'.
    """
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
    """
    Test case to verify the filtering of programs by state.

    This test case checks if the 'programas' view correctly filters programs based on the provided state.
    It creates instances of programs with different states, sets the state filter to 'Aprobado' (assuming the ID of 'Aprobado' state is 1),
    authenticates the user, and sends a GET request to the 'programas' view. It then asserts that the response status code is 200,
    and checks if the expected programs are present or not in the response content.

    """
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
    """
    Test case to verify the filtering of programs by faculty.

    This test case creates instances of programs and sets up a request with a faculty ID.
    It then authenticates the user, makes a request to the 'programas' view, and checks the response.

    The expected behavior is that the response status code should be 200, and the content of the response
    should contain 'Programa 1' and 'Programa 3', but not 'Programa 2'.

    Preconditions:
    - The 'crear_instancias' function must be defined and set up the necessary program instances.
    - The 'autenticar_usuario' function must be defined and authenticate the user.
    - The 'programas' view must be defined and handle the request to filter programs by faculty.

    Postconditions:
    - The response status code should be 200.
    - The content of the response should contain 'Programa 1' and 'Programa 3', but not 'Programa 2'.
    """
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
