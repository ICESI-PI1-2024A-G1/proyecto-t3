from django_selenium_test import PageElement
from selenium.webdriver.common.by import By

from usuarios.tests.functional_tests.base import BaseTestCase


class TestInicio(BaseTestCase):
    def setUp(self):
        self.setup_data()
        self.create_user()
        self.login()

    def test_inicio_muestra_banner(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.TAG_NAME, "img")

    def test_inicio_muestra_estadisticas(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.CLASS_NAME, "card-title")

        estadisticas = self.selenium.find_elements(By.CLASS_NAME, "card-title")
        self.assertEqual(len(estadisticas), 4)
        self.assertEqual(estadisticas[0].text, "2")
        self.assertEqual(estadisticas[1].text, "2")
        self.assertEqual(estadisticas[2].text, "4")
        self.assertEqual(estadisticas[3].text, "2")

    def test_inicio_muestra_graficas(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.ID, "myChart")
        self.wait_for_element(By.ID, "myChartDias")

        grafica_1 = self.selenium.find_element(By.ID, "myChart")
        grafica_2 = self.selenium.find_element(By.ID, "myChartDias")

        self.assertTrue(grafica_1.is_displayed())
        self.assertTrue(grafica_2.is_displayed())

    def test_inicio_muestra_titulo(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.TAG_NAME, "h1")

        titulo = self.selenium.find_element(By.TAG_NAME, "h1")
        self.assertEqual(titulo.text, "Bienvenido al sistema de control académico")

    def test_inicio_muestra_seccion_estadisticas(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.TAG_NAME, "h2")

        seccion_estadisticas = self.selenium.find_element(By.TAG_NAME, "h2")
        self.assertEqual(seccion_estadisticas.text, "Estadísticas")