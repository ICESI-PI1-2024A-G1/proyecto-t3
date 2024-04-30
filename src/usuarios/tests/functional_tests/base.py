from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import SeleniumTestCase
from mixer.backend.django import mixer

from usuarios.models import Persona, Usuario


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class BaseTestCase(SeleniumTestCase):

    __username__ = "user"
    __password__ = "user"

    def como_gestor(self):
        grupo = mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(grupo)
        self.user.save()

    def como_lider(self):
        grupo = mixer.blend("auth.Group", name="lideres")
        self.user.groups.add(grupo)
        grupo = mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(grupo)
        self.user.save()

    def como_director(self):
        grupo = mixer.blend("auth.Group", name="directores")
        self.user.groups.add(grupo)
        self.user.save()

    def como_banner(self):
        grupo = mixer.blend("auth.Group", name="banner")
        self.user.groups.add(grupo)
        self.user.save()

    def como_administrador(self):
        self.como_lider()
        self.user.is_superuser = True
        self.user.save()
        
    def create_user(self):
        self.user = User.objects.create_user(self.__username__, "user@example.com", self.__password__)

        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)
        

    def login(self):
        self.selenium.get(self.live_server_url)
        self.selenium.login(username=self.__username__, password=self.__password__)

