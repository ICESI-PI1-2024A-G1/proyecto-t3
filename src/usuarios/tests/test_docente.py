import pytest
from django.test import RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from usuarios.models import (Ciudad, Contrato, Director, Docente, EstadoContrato,
                     EstadoDocente, Persona, TipoContrato)
from usuarios.views import docente_Detail