from datetime import datetime
from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from usuarios.tests.functional_tests.base import BaseTestCase

from usuarios.models import Persona, Usuario, Ciudad
from academico.models import (Clase, Curso, Departamento, Docente, Espacio, MallaCurricular,
                              Materia, Modalidad, Periodo, TipoDeMateria, Facultad, Director, EstadoSolicitud, TipoDePrograma, Programa)
from academico.views import crear_clase, eliminar_clase


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class LoginPageTestCase(BaseTestCase):

    def setUp(self):

        self.user = User.objects.create_user("user", "user@example.com", "user")
        grupo = mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(grupo)
        self.user.save()
        
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)


        cali = Ciudad.objects.create(ciudad="Cali")
        facultadA = Facultad.objects.create(nombre="Facultad A")
        director = Director.objects.create(
        cedula="123456",
        nombre="juan",
        email="juan@gmail.com",
        telefono="123456",
        ciudad=cali,
        fechaNacimiento="2021-01-01",
        oficina="oficina",
        )
        aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
        maestria = TipoDePrograma.objects.create(nombre="Maestria")
        programa = Programa.objects.create(
        codigo="P1",
        nombre="Programa 1",
        facultad=facultadA,
        director=director,
        estado_solicitud=aprobado,
        tipo_de_programa=maestria,
        )

        
        periodo_semestre = Periodo.objects.create(semestre='202402', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
        departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
        tipo_materia = TipoDeMateria.objects.create(tipo="1")
        materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
        curso = Curso.objects.create(grupo = '4', cupo = 30, materia_id=materia, periodo_id="202402")


        







    

    def test_crear_clase(self):
    # Iniciar sesión primero
        self.selenium.get(self.live_server_url + '/login')
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()


        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias')
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()
        
        cursos = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        cursos[0].click()
        


    

        


