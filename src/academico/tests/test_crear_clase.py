from django.test import TestCase, Client
from django.urls import reverse
from academico.models import Docente, Curso, Espacio, Modalidad, Clase
from academico.views import crear_clase
import pytest


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