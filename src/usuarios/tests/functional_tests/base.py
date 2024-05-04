from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import SeleniumTestCase
from mixer.backend.django import mixer

from academico.models import (Clase, Curso, Espacio, EspacioClase,
                              GrupoDeClase, MallaCurricular, Materia, Periodo,
                              Programa)
from usuarios.models import Director, Docente, Persona, Usuario


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

        if not self.initial_db.get("persona"):
            self.initial_db["persona"] = mixer.blend(Persona)
        mixer.blend(Usuario, persona=self.initial_db["persona"], usuario=self.user)

    def login(self):
        self.selenium.get(self.live_server_url)
        self.selenium.login(username=self.__username__, password=self.__password__)

    def setup_data(self):
        # Crear un programa de prueba
        self.initial_db = {}
        self.setup_programas()
        self.setup_materias()
        self.setup_clases()

    def setup_programas(self):
        if not self.initial_db.get("persona"):
            self.initial_db["persona"] = mixer.blend(Persona)
        self.initial_db["director_1"] = mixer.blend(Director, persona=self.initial_db["persona"])
        self.initial_db["director_2"] = mixer.blend(Director)

        self.initial_db["docente_1"] = mixer.blend(Docente)
        self.initial_db["docente_2"] = mixer.blend(Docente)

        espera = mixer.blend("academico.EstadoSolicitud", nombre="En espera")
        mixer.blend("academico.EstadoSolicitud", nombre="En proceso")
        mixer.blend("academico.EstadoSolicitud", nombre="Por aprobar")
        mixer.blend("academico.EstadoSolicitud", nombre="Aprobado")
        mixer.blend("academico.EstadoSolicitud", nombre="Rechazado")
        mixer.blend("academico.EstadoSolicitud", nombre="Cancelado")

        self.initial_db["programa_1"] = mixer.blend(Programa, estado_solicitud=espera, director=self.initial_db["director_1"])
        self.initial_db["programa_2"] = mixer.blend(Programa, estado_solicitud=espera, director=self.initial_db["director_2"])

    def setup_materias(self):
        self.initial_db["materia_1"] = mixer.blend(Materia, creditos=1)
        self.initial_db["materia_2"] = mixer.blend(Materia, creditos=2)
        self.initial_db["materia_3"] = mixer.blend(Materia, creditos=2)
        self.initial_db["materia_4"] = mixer.blend(Materia, creditos=1)

        self.initial_db["periodo_1"] = mixer.blend(Periodo, semestre="2021-1")
        self.initial_db["periodo_2"] = mixer.blend(Periodo, semestre="2021-2")

        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_1"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_2"], periodo=self.initial_db["periodo_1"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_3"], periodo=self.initial_db["periodo_1"], semestre=2)

        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_2"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_2"], periodo=self.initial_db["periodo_2"], semestre=2)

        mixer.blend(MallaCurricular, programa=self.initial_db["programa_2"], materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_1"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_2"], materia=self.initial_db["materia_2"], periodo=self.initial_db["periodo_1"], semestre=1)

    def setup_clases(self):
        self.initial_db["curso_1"] = mixer.blend(Curso, materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_1"])

        self.initial_db["grupo_clase_1"] = mixer.blend(GrupoDeClase)
        self.initial_db["grupo_clase_2"] = mixer.blend(GrupoDeClase)

        self.initial_db["espacio_clase_1"] = mixer.blend(EspacioClase)
        self.initial_db["espacio_clase_2"] = mixer.blend(EspacioClase)

        self.initial_db["clase_1"] = mixer.blend(Clase, grupo_clases=self.initial_db["grupo_clase_1"], espacio_asignado=self.initial_db["espacio_clase_1"], curso=self.initial_db["curso_1"], docente=self.initial_db["docente_1"])
        self.initial_db["clase_2"] = mixer.blend(Clase, grupo_clases=self.initial_db["grupo_clase_2"], espacio_asignado=self.initial_db["espacio_clase_2"], curso=self.initial_db["curso_1"], docente=self.initial_db["docente_1"])
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

    def setup_data(self):
        # Crear datos de prueba
        # Por implementar
        pass
        
