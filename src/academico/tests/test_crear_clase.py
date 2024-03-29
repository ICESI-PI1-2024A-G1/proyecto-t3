from django.contrib.auth.models import User
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.test import TestCase, Client
from django.urls import reverse
from academico.models import Docente, Curso, Espacio, Modalidad, Clase
from academico.views import crear_clase
import pytest
import pytest


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
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('crear_clase', kwargs={'curso_id': 1}))
    request.user = user
    return request

@pytest.fixture
def curso(db):
    """
    Fixture que crea y retorna un objeto de tipo Curso para ser utilizado en pruebas.

    Args:
        db: Objeto de la base de datos.

    Returns:
        Curso: Objeto de tipo Curso creado para pruebas.
    """
    periodo = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
    curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id = 1, periodo = periodo)
    return curso

@pytest.mark.django_db
def test_crear_clase_post_negativo(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        
    }
    with pytest.raises(Http404):
        crear_clase(request, curso.id)
    
    
@pytest.mark.django_db
def test_crear_clase_post_positivo(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        
    }
    response = crear_clase(request, curso.id)
    assert response.status_code == 302
    
@pytest.mark.django_db
def test_crear_clase_post_positivo_docente_null(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        
    }
    response = crear_clase(request, curso.id)
    assert response.status_code == 302
    
@pytest.mark.django_db
def test_crear_clase_post_positivo_espacio_null(autenticacion, curso):
    request = autenticacion
    request.method = 'POST'
    request.post = {
        
    }
    response = crear_clase(request, curso.id)
    assert response.status_code == 302
class CrearClaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.docente = Docente.objects.create(cedula='12345678')
        self.curso = Curso.objects.create(nrc='1')
        self.espacio = Espacio.objects.create(id=1)
        self.modalidad = Modalidad.objects.create(id=1)
        self.url = reverse('crear_clase', args=[self.curso.nrc])

    def test_crear_clase(self):
        response = self.client.post(self.url, {
            'start_day': '2022-12-01T13:15',
            'end_day': '2022-12-01T15:15',
            'tipo_espacio': self.espacio.id,
            'modalidad_clase': self.modalidad.id,
            'num_semanas': 2,
            'docente_clase': self.docente.cedula
        })
        self.assertEqual(response.status_code, 302)  # Redireccionamiento a "visualizar clases"
        self.assertEqual(Clase.objects.count(), 2)  # Se crearon 2 clases