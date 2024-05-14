from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase


class TestListadoProgramas(BaseTestCase):
    """
    Clase de prueba para el listado de programas.
    """

    search_input = PageElement(By.ID, 'q')
    img_buscar_btn = PageElement(By.XPATH, '//img[@alt="Buscar"]')
    filtrar_btn = PageElement(By.CSS_SELECTOR, 'button[type="submit"]')
    ordenar_por_select = PageElement(By.ID, 'ordenar_por')
    estado_select = PageElement(By.NAME, 'estado')

    def setUp(self):
        """
        Configura el entorno de prueba antes de ejecutar cada caso de prueba.

        Este método se ejecuta antes de cada caso de prueba y se utiliza para configurar los datos de prueba,
        crear un usuario y realizar el inicio de sesión necesario para las pruebas funcionales.
        """
        self.setup_data()
        self.create_user()
        self.login()
    
    def test_listado_programas_busqueda_por_nombre_existente_director(self):
        """
        Prueba que verifica la funcionalidad de búsqueda de programas por nombre de director existente.

        Esta prueba simula el comportamiento de un líder que realiza una búsqueda de programas por el nombre de un director existente.
        Se espera que la página de resultados muestre únicamente los programas asociados al director buscado y no muestre los programas asociados a otros directores.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["director_1"].nombre)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["director_1"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["director_2"].nombre, self.selenium.page_source)

    def test_listado_programas_filtrado_por_estado(self):
        """
        Prueba que verifica el filtrado de programas por estado de solicitud.

        Esta prueba simula el comportamiento de un líder al filtrar los programas
        por estado de solicitud. Verifica que los programas que se muestran en la
        lista correspondan al estado seleccionado.

        """
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
        """
        Prueba que verifica el listado de programas sin ningún orden específico después de aplicar un filtro.

        Esta prueba simula el comportamiento de un líder al acceder a la página de listado de programas.
        Luego, selecciona la opción "Sin orden" en el campo de ordenamiento y hace clic en el botón de filtrar.
        Después de aplicar el filtro, verifica que los nombres de los programas "programa_1" y "programa_2"
        estén presentes en la página.

        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "ordenar_por")
        Select(self.ordenar_por_select).select_by_visible_text("Sin orden")
        self.filtrar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["programa_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["programa_2"].nombre, self.selenium.page_source)

    def test_listado_programas_busqueda_por_nombre_existente_programa(self):
        """
        Prueba que verifica la funcionalidad de búsqueda por nombre existente de un programa en el listado de programas.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys(self.initial_db["programa_2"].nombre)
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertIn(self.initial_db["programa_2"].nombre, self.selenium.page_source)
        self.assertNotIn(self.initial_db["programa_1"].nombre, self.selenium.page_source)

    def test_listado_programas_busqueda_por_nombre_director_inexistente(self):
        """
        Prueba que verifica que no se encuentre un programa en el listado al buscar por el nombre de un director inexistente.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("director_10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("director_10", self.selenium.page_source)

    def test_listado_programas_busqueda_por_nombre_programa_inexistente(self):
        """
        Prueba que verifica que al buscar un programa inexistente por su nombre,
        este no se encuentre en la página de listado de programas.
        """
        self.como_lider()

        self.selenium.get(self.live_server_url + "/academico/programas")
        self.wait_for_element(By.ID, "q")
        self.search_input.send_keys("programa_10")
        self.img_buscar_btn.click()
        self.wait_for_element(By.ID, "q")
        self.assertNotIn("programa_10", self.selenium.page_source)
        
        