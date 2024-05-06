from datetime import datetime
from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase

class TestListadoDocentes(BaseTestCase):
    search_input = PageElement(By.ID, 'q')
    date_input = PageElement(By.ID, 'q2')
    img_buscar_btn = PageElement(By.XPATH, '//img[@alt="Buscar"]')
    filtrar_btn = PageElement(By.CSS_SELECTOR, 'button[type="submit"]')
    ordenar_por_select = PageElement(By.ID, 'ordenar_por')
    hospedaje_select = PageElement(By.NAME, 'hospedaje')

    def setUp(self):
        self.setup_data4()
        self.create_user()
        self.login()
    
    def test_listado_viaticos_busqueda_por_clase_existente(self):
        self.como_gestor()

        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["viatico_1"].clase.id)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(str(self.initial_db["viatico_1"].clase.id), self.selenium.page_source)
        self.assertNotIn(str(self.initial_db["viatico_2"].clase.id), self.selenium.page_source)

    def test_listado_viaticos_busqueda_por_clase_inexistente(self):
        self.como_gestor()

        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("clase10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("clase10", self.selenium.page_source)

    
    def test_listado_viaticos_filtrado_sin_orden(self):
        self.como_gestor()

        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Sin orden")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(str(self.initial_db["viatico_1"].clase.id), self.selenium.page_source)
        self.assertIn(str(self.initial_db["viatico_2"].clase.id), self.selenium.page_source)


    