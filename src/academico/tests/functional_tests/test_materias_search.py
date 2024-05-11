from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

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
        """
        Configura el entorno de prueba creando datos necesarios, un usuario y realizando el inicio de sesión.
        """
        self.setup_data5()
        self.create_user()
        self.login()
        

        

    def test_filtrado_positivo_lista_filtrada(self):
        """
        Prueba la funcionalidad de filtrado positivo cuando la lista está filtrada según un departamento.
        
        Args:
            None

        Returns:
            None
        """
        
        self.como_lider()

        self.selenium.get(self.live_server_url)
        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        #Llenar form para filrado
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(self.initial_db["materia_1"].departamento.nombre)
        
        # Press Enter key
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(Keys.ENTER)


        # Validar que se redirigió a la página de inicio
        self.assertNotIn(self.initial_db["materia_2"].departamento.nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_1"].departamento.nombre, self.selenium.page_source)
        
    def test_filtrado_positivo_lista_Vacia(self):
        """
        Prueba la funcionalidad de filtrado positivo cuando la lista está filtrada y resulta vacia.
        
        Args:
            None

        Returns:
            None
        """
        self.como_lider()

        self.selenium.get(self.live_server_url)
        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        #Llenar form para filrado
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(self.initial_db["departamento_4"].nombre)
        
        # Press Enter key
        self.wait_for_element(By.ID, "q")
        self.search.send_keys(Keys.ENTER)

        self.assertNotIn(self.initial_db["materia_1"].departamento.nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["materia_2"].departamento.nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["materia_3"].departamento.nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["materia_4"].departamento.nombre, self.selenium.page_source)
        
    def test_filtrado_positivo_no_filtrada(self):
        """
        Prueba la funcionalidad de filtrado positivo cuando la lista no está filtrada.
        
        Args:
            None

        Returns:
            None
        """
        self.como_lider()

        self.selenium.get(self.live_server_url)
        
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
        self.assertIn(self.initial_db["materia_1"].departamento.nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_2"].departamento.nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_3"].departamento.nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_4"].departamento.nombre, self.selenium.page_source)