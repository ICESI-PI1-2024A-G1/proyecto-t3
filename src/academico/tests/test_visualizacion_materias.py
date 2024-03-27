from django.http import Http404
import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from mixer.backend.django import mixer
from academico.models import Curso, Clase, Departamento, Materia, Modalidad, Periodo, TipoDeMateria, Espacio
from academico.views import visualizacion_curso
from datetime import datetime

pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def autenticacion(db, rf):
    user = User.objects.create_user(username='admin', password='admin')
    request = rf.get(reverse('visualizacion_materias', kwargs={'materia.codigo': 101}))
    request.user = user
    return request