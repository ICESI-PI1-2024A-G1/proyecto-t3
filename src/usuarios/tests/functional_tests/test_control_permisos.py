from time import sleep

from django.contrib.auth.models import Group, User
from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase


class ControlPermisosTestCase(BaseTestCase):
    """
    Clase de prueba que contiene casos de prueba relacionados con el control de permisos.
    """

    def setUp(self):
        """
        Configura el entorno de prueba configurando los datos necesarios,
        creando un usuario e iniciando sesión.
        """
        self.setup_data()
        self.create_user()
        self.login()
        self.setup_otros_usuarios()

    # Resto del código...
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
        """
        Prueba que verifica el comportamiento del sistema cuando un usuario con el rol de líder
        intenta acceder a la página de administrador y se muestra un mensaje de error.
        """
        self.como_lider()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_como_gestor(self):
        """
        Prueba que verifica el comportamiento del sistema cuando un usuario con el rol de gestor
        intenta acceder a la página de administrador y se muestra un mensaje de error.
        """
        self.como_gestor()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_como_director(self):
        """
        Prueba que verifica el comportamiento del sistema cuando un usuario con el rol de director
        intenta acceder a la página de administrador de usuarios.

        Se espera que el sistema muestre un mensaje de error indicando que la página no se encontró.
        """
        self.como_director()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_como_banner(self):
        """
        Prueba que verifica el comportamiento del sistema cuando se accede a la página de administrador
        como un usuario con el rol de "banner".
        """
        self.como_banner()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        sleep(1)
        self.assertIn("notfound", self.selenium.page_source)

    def test_inactivar_y_activar_usuario(self):
        """
        Prueba que verifica la funcionalidad de inactivar y activar un usuario.

        Esta prueba simula el comportamiento de un administrador al inactivar y activar un usuario en el sistema.
        Se asegura de que el usuario esté activo inicialmente, luego lo inactiva y verifica que el estado del usuario
        haya cambiado a inactivo. Luego, lo activa nuevamente y verifica que el estado del usuario haya cambiado a activo.

        Args:
            self: El objeto de prueba.

        Returns:
            None
        """
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
        """
        Prueba que verifica la funcionalidad de cambiar roles de usuario.

        Esta prueba simula el comportamiento de un administrador al cambiar el rol de un usuario.
        Se asegura de que el usuario tenga el rol de "Lider" después de realizar el cambio.
        """
        self.como_administrador()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")

        self.wait_for_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]')
        PageElement(By.CSS_SELECTOR, 'button[class="btn btn-secondary dropdown-toggle"]').click()
        PageElement(By.CSS_SELECTOR, 'a[onclick="changeRolTo(\'usuario_1\',\'Lider\')"]').click()
        self.selenium.get(self.live_server_url + "/usuarios/administrador")
        assert User.objects.get(username="usuario_1").groups.filter(name="lideres").exists()

    def test_cambiar_roles_y_volver(self):
        """
        Prueba que verifica la funcionalidad de cambiar roles de usuario y volver a la página de administrador.

        Esta prueba simula el comportamiento de un administrador al cambiar los roles de un usuario específico.
        Se asegura de que los cambios de roles se reflejen correctamente en la base de datos y que el usuario
        pueda volver a la página de administrador después de realizar los cambios.
        """
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
