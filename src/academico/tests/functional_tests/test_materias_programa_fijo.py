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
        """
        Configura el entorno de prueba creando datos necesarios, un usuario y realizando el inicio de sesión.
        """
        self.setup_data5()
        self.create_user()
        self.login()
        
        

        

    def test_filtrado_positivo_lista_filtrada(self):
        """
        Prueba la funcionalidad de filtrado positivo cuando la lista está filtrada según un programa.
        
        Args:
            None

        Returns:
            None
        """

        self.como_lider()

        # Visitar la página
        self.selenium.get(self.live_server_url)
        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        self.wait_for_element(By.ID, "filtrar_por_programa")
        self.filtrar_por_programa.click()
        
         # Seleccionar el programa correcto de la lista desplegable
        programa1 = PageElement(By.ID,  self.initial_db["programa_1"].nombre + " select")
        self.wait_for_element(By.ID, self.initial_db["programa_1"].nombre + " select")
        programa1.click()
        
        self.wait_for_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.filtrar_btn.click()
        

        self.assertNotIn(self.initial_db["materia_4"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_2"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_3"].nombre, self.selenium.page_source)

    def test_filtrado_positivo_lista_Vacia(self):
        """
        Prueba la funcionalidad de filtrado positivo cuando la lista está filtrada y vacía.
        
        Args:
            None

        Returns:
            None
        """

        self.como_lider()

        # Visitar la página
        self.selenium.get(self.live_server_url)

        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        self.wait_for_element(By.ID, "filtrar_por_programa")
        self.filtrar_por_programa.click()
        
         # Seleccionar el programa correcto de la lista desplegable
        programa3 = PageElement(By.ID,  self.initial_db["programa_3"].nombre + " select")
        self.wait_for_element(By.ID, self.initial_db["programa_3"].nombre + " select")
        programa3.click()
        
        self.wait_for_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.filtrar_btn.click()
        

        self.assertNotIn(self.initial_db["materia_4"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["materia_2"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["materia_3"].nombre, self.selenium.page_source)


    def test_filtrado_positivo_lista_no_filtrada(self):
        """
        Prueba la funcionalidad de filtrado positivo cuando la lista no está filtrada.
        
        Args:
            None

        Returns:
            None
        """

        self.como_lider()
        
        # Visitar la página
        self.selenium.get(self.live_server_url)

        
        # Buscar listado de sidebar
        self.wait_for_element(By.ID, "Materias posgrado btn")
        self.lista_materias.click()
        
        self.wait_for_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.filtrar_btn.click()
        

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias?programa="
        )
        self.assertIn(self.initial_db["materia_4"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_2"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["materia_3"].nombre, self.selenium.page_source)