from django.test import TestCase, Client
from django.urls import reverse
from academico.models import Curso
from solicitud.models import Usuario
from django.contrib.auth.models import User
from academico.models import (Clase, Curso, Departamento, Docente, Espacio,
                              Materia, Modalidad, Periodo, TipoDeMateria)
from academico.views import (crear_clase, solicitar_salones)
from solicitud.models import (SolicitudEspacio, Usuario, EstadoSolicitud, SolicitudClases)


class SolicitarSalonesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(nrc='12345', nombre='Test Course')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.usuario = Usuario.objects.create(user=self.user, nombre='Test User')
        self.url = reverse('solicitar_salones', args=[self.curso.nrc])

    def test_solicitar_salones_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_solicitar_salones_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)

    def test_solicitar_salones_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
