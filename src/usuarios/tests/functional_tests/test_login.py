from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By

from usuarios.models import Persona, Usuario


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class LoginPageTestCase(SeleniumTestCase):

    username = PageElement(By.ID, "username")
    password = PageElement(By.ID, "password")
    submit = PageElement(By.ID, "submit")
    logout = PageElement(By.ID, "logout-btn")

    def setUp(self):
        self.user = User.objects.create_user("user", "user@example.com", "user")
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)

    def test_inicio_sesion_valido(self):
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/inicio"
        )
        self.assertIn("Bienvenido", self.selenium.page_source)

    def test_inicio_sesion_contraseña_incorrecta(self):
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
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")

    def test_inicio_sesion_usuario_no_autenticado(self):
        self.selenium.get(self.live_server_url + "/academico/inicio")
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/login?next=/academico/inicio")

    def test_cerrar_sesion(self):
        self.selenium.get(self.live_server_url)
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()
        self.logout.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")
        self.assertIn("Iniciar sesión", self.selenium.page_source)
