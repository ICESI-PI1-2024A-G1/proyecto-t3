from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By

from usuarios.models import Persona, Usuario
from usuarios.tests.functional_tests.base import BaseTestCase


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class LoginPageTestCase(BaseTestCase):
    """
    Clase de prueba para probar el inicio de sesión en la página de login.
    """

    username = PageElement(By.ID, "username")
    password = PageElement(By.ID, "password")
    submit = PageElement(By.ID, "submit")
    logout = PageElement(By.ID, "logout-btn")

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.user = User.objects.create_user("user", "user@example.com", "user")

        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)

    def test_inicio_sesion_valido(self):
            """
            Prueba el inicio de sesión válido.

            Esta prueba verifica el funcionamiento del inicio de sesión cuando se ingresan credenciales válidas.
            """
            # Código de la prueba
            self.como_lider()
            self.selenium.get(self.live_server_url)

            self.username.send_keys("user")
            self.password.send_keys("user")
            self.submit.click()

            self.assertEqual(
                self.selenium.current_url, self.live_server_url + "/academico/inicio"
            )
            self.assertIn("Bienvenido", self.selenium.page_source)

    def test_inicio_sesion_valido_banner(self):
        """
        Prueba que verifica el inicio de sesión válido desde el banner.

        Esta prueba simula el proceso de inicio de sesión válido desde el banner de la página.
        Se visita la página, se llena el formulario con un nombre de usuario y contraseña válidos,
        se envía el formulario y se valida que se redirija correctamente a la página de inicio.

        """
        # Visitar la página
        self.como_banner()
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/solicitud/salones_solicitud"
        )
        self.assertIn("Lista de solicitudes", self.selenium.page_source)

    def test_inicio_sesion_contraseña_incorrecta(self):
        """
        Prueba que verifica el inicio de sesión con una contraseña incorrecta.

        Esta prueba simula el proceso de inicio de sesión en la página web. Se visita la página de inicio,
        se llena el formulario con un nombre de usuario y una contraseña incorrecta, y se envía el formulario.
        Luego, se valida que se redirija a la página de inicio y que se muestre el mensaje de error indicando
        que el usuario y/o contraseña son incorrectos.
        """
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("user")
        self.password.send_keys("wrong")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")
        self.assertIn("Usuario y/o contraseña incorrectos", self.selenium.page_source)

    def test_inicio_sesion_usuario_inactivo(self):
        """
        Prueba que verifica el comportamiento del inicio de sesión cuando el usuario está inactivo.

        Esta prueba simula el escenario en el que un usuario intenta iniciar sesión en el sistema, pero su cuenta está marcada como inactiva.

        Esta prueba asegura que el sistema maneje correctamente la situación de un usuario inactivo al intentar iniciar sesión.
        """
        self.user.is_active = False
        self.user.save()
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")
        self.assertIn("Usuario y/o contraseña incorrectos", self.selenium.page_source)

    def test_inicio_sesion_usuario_no_existe(self):
        """
        Prueba que verifica el comportamiento del sistema cuando se intenta iniciar sesión con un usuario que no existe.

        Expected:
        - El sistema debe redirigir al usuario a la página de inicio.
        - Se debe mostrar un mensaje de error indicando que el usuario y/o contraseña son incorrectos.
        """
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("wrong")
        self.password.send_keys("wrong")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")
        self.assertIn("Usuario y/o contraseña incorrectos", self.selenium.page_source)

    def test_inicio_sesion_campos_vacios(self):
        """
        Prueba que verifica el comportamiento cuando se intenta iniciar sesión con campos vacíos.

        Esta prueba verifica que el sistema maneje correctamente la situación cuando se intenta iniciar sesión sin proporcionar ningún dato en los campos requeridos.
        """
        self.selenium.get(self.live_server_url)
        self.submit.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")

    def test_inicio_sesion_usuario_no_autenticado(self):
        """
        Prueba el inicio de sesión de un usuario no autenticado.

        Esta prueba verifica que cuando un usuario no autenticado intenta acceder a la página de inicio
        del módulo académico, se redirige correctamente a la página de inicio de sesión.

        """
        self.selenium.get(self.live_server_url + "/academico/inicio")
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/login?next=/academico/inicio")

    def test_cerrar_sesion(self):
        """
        Prueba que verifica el cierre de sesión de un usuario.

        Esta prueba simula el proceso de inicio de sesión de un usuario como gestor,
        luego cierra la sesión y verifica que el usuario sea redirigido a la página de inicio
        y que se muestre el mensaje "Iniciar sesión" en la página.

        """
        self.como_gestor()
        self.selenium.get(self.live_server_url)
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()
        self.logout.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")
        self.assertIn("Iniciar sesión", self.selenium.page_source)
