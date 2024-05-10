from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from usuarios.models import Persona, Usuario, Ciudad
from academico.models import Programa, Periodo, Materia, Departamento, TipoDeMateria, Director, EstadoSolicitud, Facultad, TipoDePrograma, MallaCurricular
from usuarios.tests.functional_tests.base import BaseTestCase

@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class MateriasTestCase(BaseTestCase):

    username = PageElement(By.ID, "username")
    password = PageElement(By.ID, "password")
    submit = PageElement(By.ID, "submit")
    logout = PageElement(By.ID, "logout-btn")
    lista_materias = PageElement(By.ID, "Materias posgrado btn")
    search = PageElement(By.ID, "q")
    filtro_submit = PageElement(By.ID, "filtrar_materias")

    def setUp(self):
        self.setup_data5()
        self.create_user()
        self.login()
        

        

    def test_filtrado_positivo_lista_filtrada(self):
        self.como_lider()
        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        #Llenar form para filrado
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(self.initial_db["departamento_1"].nombre)
        
        # Press Enter key
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(Keys.ENTER)

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias?q=Departamento+1"
        )
        self.assertNotIn(self.initial_db["departamento_2"].nombre, self.selenium.page_source)
        
    def test_filtrado_positivo_lista_Vacia(self):
        self.como_lider()
        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        #Llenar form para filrado
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(self.initial_db["departamento_4"].nombre)
        
        # Press Enter key
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(Keys.ENTER)

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias?q=Departamento+4"
        )
        self.assertNotIn(self.initial_db["departamento_1"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["departamento_2"].nombre, self.selenium.page_source)
        
    def test_filtrado_positivo_no_filtrada(self):
        self.como_lider()
        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        #Llenar form para filrado
        self.wait_for_element(By.ID, "q")
        self.search.send_keys("")
        
        # Press Enter key
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(Keys.ENTER)

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias?q="
        )
        self.assertIn(self.initial_db["departamento_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["departamento_2"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["departamento_3"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["departamento_4"].nombre, self.selenium.page_source)