from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase


class TestListadoProgramas(BaseTestCase):
    search_input = PageElement(By.ID, 'q')
    img_buscar_btn = PageElement(By.XPATH, '//img[@alt="Buscar"]')
    filtrar_btn = PageElement(By.CSS_SELECTOR, 'button[type="submit"]')
    ordenar_por_select = PageElement(By.ID, 'ordenar_por')
    estado_select = PageElement(By.NAME, 'estado')

    def setUp(self):
        self.setup_data()
        self.create_user()
        self.login()
    
    def test_listado_programas_busqueda_por_nombre_existente_director(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["director_1"].nombre)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["director_1"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["director_2"].nombre, self.selenium.page_source)

    def test_listado_programas_filtrado_por_estado(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Estado de Solicitud")
        self.wait_for_element(By.NAME, "estado")
        Select(self.estado_select).select_by_visible_text("En espera")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn("En espera", self.selenium.page_source)

    def test_listado_programa_filtrado_sin_orden(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Sin orden")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["programa_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["programa_2"].nombre, self.selenium.page_source)

    def test_listado_programas_busqueda_por_nombre_existente_programa(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["programa_2"].nombre)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["programa_2"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["programa_1"].nombre, self.selenium.page_source)

    def test_listado_programas_busqueda_por_nombre_director_inexistente(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("director_10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("director_10", self.selenium.page_source)

    def test_listado_programas_busqueda_por_nombre_programa_inexistente(self):
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("programa_10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("programa_10", self.selenium.page_source) 
        
        