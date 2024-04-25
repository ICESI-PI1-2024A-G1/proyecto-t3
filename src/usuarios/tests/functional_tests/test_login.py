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

    def setUp(self):
        self.user = User.objects.create_user("admin", "admin@example.com", "admin")
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)

    def test_successful_login(self):
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("admin")
        self.password.send_keys("admin")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/inicio"
        )
        self.assertIn("Bienvenido", self.selenium.page_source)

    def test_failed_login(self):
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("admin")
        self.password.send_keys("wrong")
        self.submit.click()

        # Validar que se redirigió a la página de inicio
        self.assertEqual(self.selenium.current_url, self.live_server_url + "/")
        self.assertIn("Usuario y/o contraseña incorrectos", self.selenium.page_source)
