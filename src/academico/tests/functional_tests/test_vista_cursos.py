from time import sleep
from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from solicitud.models import SolicitudViatico
from usuarios.tests.functional_tests.base import BaseTestCase


class TestVistaCursos(BaseTestCase):

    def setUp(self):
        self.setup_data()
        self.create_user()
        self.login()

    # def test_informacion_basica_curso(self):
    #     self.como_lider()
        
    #     curso_id = self.initial_db["curso_1"].nrc
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")

    #     # Información básica del curso
    #     self.assertIn(str(self.initial_db["curso_1"].nrc), self.selenium.page_source)
    #     self.assertIn(str(self.initial_db["curso_1"].grupo), self.selenium.page_source)
    #     self.assertIn(str(self.initial_db["curso_1"].cupo), self.selenium.page_source)
    #     self.assertIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
    #     self.assertIn(self.initial_db["periodo_1"].semestre, self.selenium.page_source)

    # def test_docentes_asignados(self):
    #     self.como_lider()
        
    #     curso_id = self.initial_db["curso_1"].nrc
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
        
    #     # Verifica que se muestren los docentes asignados al curso
    #     self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)

    # def test_boton_solicitar_salones(self):
    #     self.como_lider()
    #     curso_id = self.initial_db["curso_1"].nrc
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")
    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")

    #     # Verifica que se muestre el botón de solicitar salones
    #     boton_solicitar_salones = self.selenium.find_element(By.CSS_SELECTOR, "button[onclick='Solicitud_Salones()']")
    #     self.assertTrue(boton_solicitar_salones.is_displayed())

    # def test_visualizar_clases(self):
    #     self.como_lider()
    #     curso_id = self.initial_db["curso_1"].nrc
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")
    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")

    #     # Verifica que se muestren las clases del curso
    #     self.assertIn(str(self.initial_db["espacio_clase_1"].edificio),self.selenium.page_source)
    #     self.assertIn(str(self.initial_db["espacio_clase_1"].numero),self.selenium.page_source)
    #     self.assertIn(self.initial_db["docente_1"].nombre,self.selenium.page_source)


    # def test_card_clase(self):
    #     self.como_lider()
        
    #     curso_id = self.initial_db["curso_1"].nrc
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
        
    #     self.assertIn("Clases", self.selenium.page_source)

    
    # def test_cambiar_intu_generado(self):
    #     self.como_gestor()
        
    #     curso_id = self.initial_db["curso_1"].nrc
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeIntu(\'{curso_id}\')"')
    #     PageElement(By.CSS_SELECTOR, f'input[onchange="changeIntu(\'{curso_id}\')"').click()
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeIntu(\'{curso_id}\')"')
    #     self.initial_db["curso_1"].refresh_from_db()
    #     assert self.initial_db["curso_1"].intu_generado == True

    # def test_cambiar_notas_entrega(self):
    #     self.como_gestor()
        
    #     curso_id = self.initial_db["curso_1"].nrc
    #     grupo_id = self.initial_db["grupo_clase_1"].id
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeNota(\'{curso_id}\',\'{grupo_id}\')"')
    #     PageElement(By.CSS_SELECTOR, f'input[onchange="changeNota(\'{curso_id}\',\'{grupo_id}\')"').click()
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[onchange="changeNota(\'{curso_id}\',\'{grupo_id}\')"')
    #     self.initial_db["grupo_clase_1"].refresh_from_db()
    #     assert self.initial_db["grupo_clase_1"].entrega_notas == True

    # def test_crear_solicitud_viatico(self):
    #     self.como_gestor()
        
    #     curso_id = self.initial_db["curso_1"].nrc
    #     grupo_id = self.initial_db["grupo_clase_1"].id
    #     clase_id = self.initial_db["clase_1"].id
    #     self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

    #     self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
    #     self.wait_for_element(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]')
    #     PageElement(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]').click()
    #     self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
    #     PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
    #     PageElement(By.CSS_SELECTOR, f'a[onclick="show_popViatico(\'{clase_id}\')"]').click()
    #     self.wait_for_element(By.ID, "popupViaticos")
    #     sleep(2)
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[id="tiquetes"')
    #     PageElement(By.CSS_SELECTOR, f'input[id="tiquetes"').click()
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[id="hospedaje"')
    #     PageElement(By.CSS_SELECTOR, f'input[id="hospedaje"').click()
    #     self.wait_for_element(By.CSS_SELECTOR, f'input[id="alimentacion"')
    #     PageElement(By.CSS_SELECTOR, f'input[id="alimentacion"').click()
    #     self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-primary mb-5"]')
    #     PageElement(By.CSS_SELECTOR, 'button[class="btn btn-primary mb-5"]').click()
    #     sleep(2)
    #     self.wait_for_element(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]')
    #     PageElement(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]').click()
    #     self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
    #     sleep(3)
    #     PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
    #     sleep(2)
    #     dropdown_items = self.selenium.driver.find_elements(By.XPATH, f"//a[contains(@class, 'dropdown-item') and contains(@onclick, 'show_popViatico') and contains(@onclick, '{clase_id}')]")

    #     # Verificar que no hay elementos 'dropdown-item'
    #     assert len(dropdown_items) == 0
    #     solicitud = SolicitudViatico.objects.filter(clase_id=clase_id).last()
    #     assert solicitud is not None
    #     assert solicitud.tiquete and solicitud.hospedaje and solicitud.alimentacion

    def test_intento_solicitud_viatico_sin_items(self):
        self.como_gestor()
        
        curso_id = self.initial_db["curso_1"].nrc
        grupo_id = self.initial_db["grupo_clase_1"].id
        clase_id = self.initial_db["clase_1"].id
        self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

        self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
        self.wait_for_element(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]')
        PageElement(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]').click()
        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, f'a[onclick="show_popViatico(\'{clase_id}\')"]').click()
        self.wait_for_element(By.ID, "popupViaticos")
        sleep(2)
        self.wait_for_element(By.CSS_SELECTOR, f'input[id="tiquetes"')
        self.wait_for_element(By.CSS_SELECTOR, f'input[id="hospedaje"')
        self.wait_for_element(By.CSS_SELECTOR, f'input[id="alimentacion"')
        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-primary mb-5"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-primary mb-5"]').click()
        sleep(2)
        self.wait_for_element(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]')
        PageElement(By.CSS_SELECTOR, f'div[onclick="display_group(\'class_group{grupo_id}\')"]').click()
        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        sleep(3)
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        sleep(2)
        dropdown_items = self.selenium.driver.find_elements(By.XPATH, f"//a[contains(@class, 'dropdown-item') and contains(@onclick, 'show_popViatico') and contains(@onclick, '{clase_id}')]")

        # Verificar que no hay elementos 'dropdown-item'
        assert len(dropdown_items) == 1
        solicitud = SolicitudViatico.objects.filter(clase_id=clase_id).last()
        assert solicitud is None



