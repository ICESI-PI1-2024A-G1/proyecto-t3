from time import sleep

from django.contrib.auth.models import Group, User
from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase


class ControlPermisosTestCase(BaseTestCase):


    def setUp(self):
        """
        Configura el entorno de prueba configurando los datos necesarios,
        creando un usuario e iniciando sesión.
        """
        self.setup_data()
        self.create_user()
        self.login()
        self.setup_otros_usuarios()

    def test_como_lider(self):
        self.como_lider()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_como_gestor(self):
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_como_director(self):
        self.como_director()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_como_banner(self):
        self.como_banner()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_inactivar_y_activar_usuario(self):
        self.como_administrador()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        
        self.wait_for_element(By.CSS_SELECTOR, 'input[onchange="changeStateTo(\'usuario_1\')"')
        PageElement(By.CSS_SELECTOR, 'input[onchange="changeStateTo(\'usuario_1\')"').click()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")

        self.wait_for_element(By.CSS_SELECTOR, 'input[onchange="changeStateTo(\'usuario_1\')"')
        PageElement(By.CSS_SELECTOR, 'input[onchange="changeStateTo(\'usuario_1\')"').click()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        assert User.objects.get(username="usuario_1").is_active == True

    def test_cambiar_roles(self):
        self.como_administrador()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")

        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, 'a[onclick="changeRolTo(\'usuario_1\',\'Lider\')"]').click()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        assert User.objects.get(username="usuario_1").groups.filter(name="lideres").exists()

    def test_cambiar_roles_y_volver(self):
        self.como_administrador()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")

        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, 'a[onclick="changeRolTo(\'usuario_1\',\'Lider\')"]').click()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        
        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        assert User.objects.get(username="usuario_1").groups.filter(name="lideres").exists()

        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, 'a[onclick="changeRolTo(\'usuario_1\',\'Gestor\')"]').click()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")

        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        assert User.objects.get(username="usuario_1").groups.filter(name="gestores").exists()
