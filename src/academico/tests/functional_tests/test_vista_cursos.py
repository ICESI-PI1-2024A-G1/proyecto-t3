from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase


class TestVistaCursos(BaseTestCase):

    def setUp(self):
        self.setup_data()
        self.create_user()
        self.login()

    def test_informacion_basica_curso(self):
        self.como_lider()
        
        curso_id = self.initial_db["curso_1"].nrc
        self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

        self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")

        # Información básica del curso
        self.assertIn(str(self.initial_db["curso_1"].nrc), self.selenium.page_source)
        self.assertIn(str(self.initial_db["curso_1"].grupo), self.selenium.page_source)
        self.assertIn(str(self.initial_db["curso_1"].cupo), self.selenium.page_source)
        self.assertIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["periodo_1"].semestre, self.selenium.page_source)

    def test_docentes_asignados(self):
        self.como_lider()
        
        curso_id = self.initial_db["curso_1"].nrc
        self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

        self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
        
        # Verifica que se muestren los docentes asignados al curso
        self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)

    def test_boton_solicitar_salones(self):
        self.como_lider()
        curso_id = self.initial_db["curso_1"].nrc
        self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")
        self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")

        # Verifica que se muestre el botón de solicitar salones
        boton_solicitar_salones = self.selenium.find_element(By.CSS_SELECTOR, "button[onclick='Solicitud_Salones()']")
        self.assertTrue(boton_solicitar_salones.is_displayed())

    def test_visualizar_clases(self):
        self.como_lider()
        curso_id = self.initial_db["curso_1"].nrc
        self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")
        self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")

        # Verifica que se muestren las clases del curso
        self.assertIn(str(self.initial_db["espacio_clase_1"].edificio),self.selenium.page_source)
        self.assertIn(str(self.initial_db["espacio_clase_1"].numero),self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].nombre,self.selenium.page_source)


    def test_card_clase(self):
        self.como_lider()
        
        curso_id = self.initial_db["curso_1"].nrc
        self.selenium.get(self.live_server_url + f"/academico/cursos/{curso_id}")

        self.wait_for_element(By.CSS_SELECTOR, "h1.card-title")
        
        self.assertIn("Clases", self.selenium.page_source)
