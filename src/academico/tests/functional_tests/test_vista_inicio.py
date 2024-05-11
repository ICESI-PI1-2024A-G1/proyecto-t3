from django_selenium_test import PageElement
from selenium.webdriver.common.by import By

from usuarios.tests.functional_tests.base import BaseTestCase


class TestInicio(BaseTestCase):
    """
    Clase de prueba para la vista de inicio.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de la vista de inicio en el sistema de control académico.
    """

    def setUp(self):
        """
        Configura el entorno de pruebas antes de ejecutar cada caso de prueba.

        Este método se ejecuta antes de cada caso de prueba y se utiliza para configurar los datos necesarios,
        crear un usuario y realizar el inicio de sesión.
        """
        self.setup_data()
        self.create_user()
        self.login()

    def test_inicio_muestra_banner(self):
        """
        Prueba que verifica si la página de inicio muestra un banner.
        """
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.TAG_NAME, "img")

    def test_inicio_muestra_estadisticas(self):
        """
        Prueba que verifica si la página de inicio muestra las estadísticas correctamente.

        Comprueba que se muestren 4 estadísticas y que los valores sean los esperados.
        """
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
        """
        Prueba que verifica si las gráficas se muestran correctamente en la página de inicio.

        Esta prueba simula el comportamiento de un gestor y verifica que las gráficas
        identificadas por los elementos con los IDs "myChart" y "myChartDias" estén visibles
        en la página de inicio.

        Se espera que ambas gráficas estén visibles y se comprueba utilizando el método
        is_displayed() de los elementos encontrados.

        """
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.ID, "myChart")
        self.wait_for_element(By.ID, "myChartDias")

        grafica_1 = self.selenium.find_element(By.ID, "myChart")
        grafica_2 = self.selenium.find_element(By.ID, "myChartDias")

        self.assertTrue(grafica_1.is_displayed())
        self.assertTrue(grafica_2.is_displayed())

    def test_inicio_muestra_titulo(self):
        """
        Prueba que verifica si la página de inicio muestra el título correcto.

        Esta prueba simula el comportamiento de un gestor y verifica que al acceder a la página de inicio,
        se muestre el título "Bienvenido al sistema de control académico".

        """
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.TAG_NAME, "h1")

        titulo = self.selenium.find_element(By.TAG_NAME, "h1")
        self.assertEqual(titulo.text, "Bienvenido al sistema de control académico")

    def test_inicio_muestra_seccion_estadisticas(self):
        """
        Prueba para verificar que la sección 'Estadísticas' se muestra en la página de inicio.
        """
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/")
        self.wait_for_element(By.TAG_NAME, "h2")

        seccion_estadisticas = self.selenium.find_element(By.TAG_NAME, "h2")
        self.assertEqual(seccion_estadisticas.text, "Estadísticas")