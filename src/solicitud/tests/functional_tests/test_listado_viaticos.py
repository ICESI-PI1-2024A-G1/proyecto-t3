from time import sleep
from datetime import datetime
from django_selenium_test import PageElement
from django.core.exceptions import ObjectDoesNotExist
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

    def test_listado_viaticos_filtrado_por_hospedaje_true(self):
        self.como_gestor()

        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Hospedaje")
        self.wait_for_element(By.NAME, "hospedaje")
        Select(self.hospedaje_select).select_by_visible_text("Si")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(str(self.initial_db["viatico_1"].clase.id), self.selenium.page_source)
        self.assertNotIn(str(self.initial_db["viatico_2"].clase.id), self.selenium.page_source)

    def test_listado_viaticos_busqueda_por_fecha_inexistente(self):
        self.como_gestor()

        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.ID, "q")
        self.date_input.send_keys("15-01-2022")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("2022-01-15", self.selenium.page_source)

    def test_listado_viaticos_busqueda_por_fecha_existente(self):
            self.como_gestor()
            self.selenium.get(self.live_server_url + "/solicitud/viaticos")
            self.wait_for_element(By.ID, "q2")
            fecha_solicitud_2 = self.initial_db["viatico_2"].fecha_solicitud
            self.date_input.send_keys(fecha_solicitud_2.strftime("%d-%m-%Y"))
            self.img_buscar_btn.click()
            self.wait_for_element(By.ID, "q2")
            self.assertIn(str(self.initial_db["viatico_1"].clase.id), self.selenium.page_source)
            self.assertIn(str(self.initial_db["viatico_2"].clase.id), self.selenium.page_source)

    def test_cambiar_hospedaje_a_false(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        viatico_1_clase = str(self.initial_db["viatico_1"].clase.id)
        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, f'a[onclick="habilitarEdicion(event, \'{viatico_1_clase}\')"]').click()
        self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeHospedaje(\'{viatico_1_clase}\')"')
        PageElement(By.CSS_SELECTOR, f'input[onchange="changeHospedaje(\'{viatico_1_clase}\')"').click()
        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeHospedaje(\'{viatico_1_clase}\')"')
        self.initial_db["viatico_1"].refresh_from_db()
        assert self.initial_db["viatico_1"].hospedaje == False

    def test_eliminar_viatico(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        viatico1 = self.initial_db["viatico_1"]
        viatico_1_clase = str(self.initial_db["viatico_1"].clase.id)
        viatico_2_clase = str(self.initial_db["viatico_2"].clase.id)
        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, f'a[onclick="confirmarEliminarClase(event, \'{viatico_1_clase}\')"]').click()
        sleep(3)
        # Espera hasta que aparezca la alerta
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())

        # Cambia al cuadro de diálogo de alerta
        alert = self.selenium.switch_to.alert

        # Haz clic en el botón de confirmación
        alert.accept()
        sleep(3)
        self.selenium.get(self.live_server_url + "/solicitud/viaticos")
        self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeHospedaje(\'{viatico_2_clase}\')"')
        try:
            viatico1.refresh_from_db()
        except ObjectDoesNotExist:
            viatico1 = None
        assert viatico1 is None

    