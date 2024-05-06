from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from academico.models import (Departamento, Director, EstadoSolicitud,
                              Facultad, MallaCurricular, Materia, Periodo,
                              Programa, TipoDeMateria, TipoDePrograma)
from usuarios.models import Ciudad, Persona, Usuario
from usuarios.tests.functional_tests.base import BaseTestCase


class TestCrearCurso(BaseTestCase):
    
    cursoN = PageElement(By.NAME, "Nuevo curso")
    cupos = PageElement(By.ID, "cantidad_de_cupos")
    confirmar = PageElement(By.CLASS_NAME, "btn btn-primary")

    def setUp(self):
        self.create_user()
        self.login()
        
        self.departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
        self.tipo_materia = TipoDeMateria.objects.create(tipo="1")
        self.materia = Materia.objects.create(codigo=10, nombre="Materia 10", creditos=3, departamento=self.departamento, tipo_de_materia=self.tipo_materia)
    
    def test_crear_curso(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/materias/1/2021-1")
        self.cursoN.click()
        self.cupos.send_key("1")
        Select(self.confirmar).select_by_value("Crear curso").click()
        
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias/10/2021-1"
        )
        self.assertIn("Cupos:1", self.selenium.page_source)
        