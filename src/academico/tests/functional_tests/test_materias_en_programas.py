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


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class MateriasTestCase(BaseTestCase):

    username = PageElement(By.ID, "username")
    password = PageElement(By.ID, "password")
    submit = PageElement(By.ID, "submit")
    logout = PageElement(By.ID, "logout-btn")
    lista_materias = PageElement(By.ID, "Materias posgrado btn")
    filtrar_por_programa = PageElement(By.ID, "filtrar_por_programa")
    filtrar_btn = PageElement(By.CSS_SELECTOR, 'button[type="submit"]')

    def setUp(self):
        self.user = User.objects.create_user("user", "user@example.com", "user")
        grupo = mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(grupo)
        self.user.save()
        
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)
        
        self.departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
        self.departamento2 = Departamento.objects.create(codigo=2, nombre="Departamento 2")
        self.tipo_materia = TipoDeMateria.objects.create(tipo="1")
        self.periodo = Periodo.objects.create(semestre="202101", fecha_inicio="2021-01-01", fecha_fin="2021-06-30")
        
        self.cali = Ciudad.objects.create(ciudad="Cali")
        self.facultadA = Facultad.objects.create(nombre="Facultad A")
        self.director = Director.objects.create(
            cedula="123456",
            nombre="juan",
            email="juan@gmail.com",
            telefono="123456",
            ciudad=self.cali,
            fechaNacimiento="2021-01-01",
            oficina="oficina",
        )
        self.aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
        self.maestria = TipoDePrograma.objects.create(nombre="Maestria")
        self.programa = Programa.objects.create(
            codigo="P1",
            nombre="Programa 1",
            facultad=self.facultadA,
            director=self.director,
            estado_solicitud=self.aprobado,
            tipo_de_programa=self.maestria,
        )
        
        Programa.objects.create(
            codigo="P2",
            nombre="Programa 2",
            facultad=self.facultadA,
            director=self.director,
            estado_solicitud=self.aprobado,
            tipo_de_programa=self.maestria,
        )
        
        self.programa3 = Programa.objects.create(
            codigo="P3",
            nombre="Programa 3",
            facultad=self.facultadA,
            director=self.director,
            estado_solicitud=self.aprobado,
            tipo_de_programa=self.maestria,
        )
        
        self.materia = Materia.objects.create(codigo=1, nombre="Materia 1", creditos=3, departamento=self.departamento, tipo_de_materia=self.tipo_materia)
        self.materia2 = Materia.objects.create(codigo=2, nombre="Materia 2", creditos=4, departamento=self.departamento2, tipo_de_materia=self.tipo_materia)
        
        MallaCurricular.objects.create(materia = self.materia, programa = self.programa, periodo = self.periodo, semestre="202101")
        MallaCurricular.objects.create(materia = self.materia2, programa = self.programa3, periodo = self.periodo, semestre="202101")
        
        

        

    def test_filtrado_positivo_lista_filtrada(self):
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()
        
        # Buscar listado de sidebar
        self.lista_materias.click()
        
        self.filtrar_por_programa.click()
        
         # Seleccionar el programa correcto de la lista desplegable
        Select(self.filtrar_por_programa).select_by_index(1)
        
        self.filtrar_btn.click()
        

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias?programa=P1"
        )
        self.assertNotIn("Materia 2", self.selenium.page_source)