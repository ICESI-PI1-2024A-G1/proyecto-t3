from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase

class TestListadoDocentes(BaseTestCase):
    search_input = PageElement(By.ID, 'q')
    img_buscar_btn = PageElement(By.XPATH, '//img[@alt="Buscar"]')
    filtrar_btn = PageElement(By.CSS_SELECTOR, 'button[type="submit"]')
    ordenar_por_select = PageElement(By.ID, 'ordenar_por')
    contrato_select = PageElement(By.NAME, 'contrato')

    def setUp(self):
        """
        Configura el entorno de prueba configurando los datos necesarios,
        creando un usuario e iniciando sesión.
        """
        self.setup_data2()
        self.create_user()
        self.login()
    
    def test_listado_docentes_busqueda_por_nombre_existente_docente(self):
        """
        Prueba funcional que verifica el resultado correspondiente a buscar a un docente existente, en la vista de listado de docentes, 
        por el nombre.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/usuarios/docentes")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["docente_1"].nombre)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["docente_2"].nombre, self.selenium.page_source)

    def test_listado_docentes_filtrado_por_contrato(self):
        """
        Prueba funcional que verifica el resultado correspondiente a filtrar el listado de docentes por su tipo de contrato.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/usuarios/docentes")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Tipo de contrato")
        self.wait_for_element(By.NAME, "contrato")
        Select(self.contrato_select).select_by_visible_text("Tiempo Completo")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn("Tiempo Completo", self.selenium.page_source)

    def test_listado_docentes_filtrado_sin_orden(self):
        """
        Prueba funcional que verifica la muestra de todos los docentes que se tiene en la base de datos, pues su indicador de filtrado
        establece que no hay orden.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/usuarios/docentes")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Sin orden")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_2"].nombre, self.selenium.page_source)

    def test_listado_docentes_busqueda_por_cedula_existente(self):
        """
        Prueba funcional que verifica el resultado correspondiente a buscar a un docente existente, en la vista de listado de docentes, 
        por la cédula.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/usuarios/docentes")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["docente_2"].cedula)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["docente_2"].cedula, self.selenium.page_source)
        self.assertNotIn(self.initial_db["docente_1"].cedula, self.selenium.page_source)

    def test_listado_docentes_busqueda_por_nombre_docente_inexistente(self):
        """
        Prueba funcional que verifica el resultado correspondiente a buscar a un docente, en la vista de listado de docentes, 
        por un nombre que no coincida con algún docente registrado.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/usuarios/docentes")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("docente_10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("docente_10", self.selenium.page_source)

    def test_listado_docentes_busqueda_por_docente_cedula_inexistente(self):
        """
        Prueba funcional que verifica el resultado correspondiente a buscar a un docente, en la vista de listado de docentes, 
        por una cédula que no coincida con algún docente registrado.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/usuarios/docentes")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("docente_10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("docente_10", self.selenium.page_source)