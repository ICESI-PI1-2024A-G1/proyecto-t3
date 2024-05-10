from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import Group, User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By

from academico.models import (Clase, Curso, Espacio, EspacioClase,
                              GrupoDeClase, MallaCurricular, Materia, Periodo,
                              Programa, Departamento)
from usuarios.models import Director, Docente, Persona, Usuario
from solicitud.models import (SolicitudViatico,SolicitudEspacio,Solicitud,EstadoSolicitud,SolicitudClases)


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class BaseTestCase(SeleniumTestCase):

    __username__ = "user"
    __password__ = "user"

    def wait_for_element(self, by, value):
        element = PageElement(by, value)
        element.wait_until_exists(10)

    def wait_for_text_in_element(self, by, value, text):
        element = PageElement(by, value)
        element.wait_until_contains(text, 10)

    def como_gestor(self):
        if not Group.objects.filter(name="gestores").exists():
            mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(Group.objects.get(name="gestores"))
        self.user.save()

    def como_lider(self):
        self.como_gestor()
        if not Group.objects.filter(name="lideres").exists():
            mixer.blend("auth.Group", name="lideres")
        self.user.groups.add(Group.objects.get(name="lideres"))
        self.user.save()

    def como_director(self):
        if not Group.objects.filter(name="directores").exists():
            mixer.blend("auth.Group", name="directores")
        self.user.groups.add(Group.objects.get(name="directores"))
        self.user.save()

    def como_banner(self):  
        if not Group.objects.filter(name="lideres").exists():
            mixer.blend("auth.Group", name="banner")
        self.user.groups.add(Group.objects.get(name="banner"))
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
        self.setup_roles()
        #self.setup_docentes()

    def setup_data2(self):
        # Crear un docente de prueba
        self.initial_db = {}
        self.setup_roles()
        self.setup_docentes()

    def setup_data3(self):
        self.initial_db = {}
        self.setup_roles()
        self.setup_materias2()
    
    def setup_data4(self):
        self.initial_db = {}
        self.setup_roles()
        self.setup_viaticos()
        
    def setup_data5(self):
        self.initial_db = {}
        self.setup_roles()
        self.setup_programas()
        self.setup_materias3()

    
        

    def setup_roles(self):
        if not Group.objects.filter(name="lideres").exists():
            mixer.blend("auth.Group", name="lideres")

        if not Group.objects.filter(name="directores").exists():
            mixer.blend("auth.Group", name="directores")

        if not Group.objects.filter(name="gestores").exists():
            mixer.blend("auth.Group", name="gestores")

        if not Group.objects.filter(name="banner").exists():
            mixer.blend("auth.Group", name="banner")

    def setup_programas(self):
        mixer.blend("usuarios.Ciudad")
        mixer.blend("usuarios.Ciudad")
        mixer.blend("usuarios.Ciudad")
        mixer.blend("usuarios.Ciudad")
        mixer.blend("usuarios.Ciudad")

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

    def setup_otros_usuarios(self):
        self.setup_roles()
        
        usuario = User.objects.create_user("usuario_1", "usuario_1@example.com", "usuario_1")
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=usuario)
        
        usuario.groups.add(Group.objects.get(name="gestores"))
        

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

        self.initial_db["clase_1"] = mixer.blend(Clase, grupo_clases=self.initial_db["grupo_clase_1"], espacio_asignado=self.initial_db["espacio_clase_1"], curso=self.initial_db["curso_1"], docente=self.initial_db["docente_1"], fecha_inicio="2021-01-01", fecha_fin="2021-01-01")
        self.initial_db["clase_2"] = mixer.blend(Clase, grupo_clases=self.initial_db["grupo_clase_2"], espacio_asignado=self.initial_db["espacio_clase_2"], curso=self.initial_db["curso_1"], docente=self.initial_db["docente_1"], fecha_inicio="2021-01-01", fecha_fin="2021-01-01")

    def setup_docentes(self):
        tiempoCompleto = mixer.blend("usuarios.TipoContrato", tipo="Tiempo Completo")
        tiempoParcial = mixer.blend("usuarios.TipoContrato", tipo="Tiempo Parcial")
        contratoA = mixer.blend("usuarios.Contrato", tipo_contrato=tiempoCompleto)
        contratoB = mixer.blend("usuarios.Contrato", tipo_contrato=tiempoParcial)
        mixer.blend("usuarios.TipoContrato", tipo="Contrato de Obra o Labor")
        mixer.blend("usuarios.TipoContrato", tipo="Contrato de Aprendizaje")
        mixer.blend("usuarios.TipoContrato", tipo="Contrato de Pretación de Servicios")
        mixer.blend("usuarios.TipoContrato", tipo="Contrato de Práctica Laboral")

        self.initial_db["docente_1"] = mixer.blend(Docente, cedula="12345", nombre="juan",contrato_codigo=contratoA)
        self.initial_db["docente_2"] = mixer.blend(Docente, cedula="11111", nombre="ana",contrato_codigo=contratoB)

    def setup_materias2(self):
        self.setup_docentes()
        self.initial_db["materia_1"] = mixer.blend(Materia, creditos=1)
        self.initial_db["materia_2"] = mixer.blend(Materia, creditos=2)
        self.initial_db["materia_3"] = mixer.blend(Materia, creditos=2)
        self.initial_db["materia_4"] = mixer.blend(Materia, creditos=1)

        self.initial_db["periodo_1"] = mixer.blend(Periodo, semestre="20211")
        self.initial_db["periodo_2"] = mixer.blend(Periodo, semestre="20212")
        self.setup_clases()
    def setup_clases2(self):
            self.initial_db["curso_1"] = mixer.blend(Curso, materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_1"])

            self.initial_db["grupo_clase_1"] = mixer.blend(GrupoDeClase)
            self.initial_db["grupo_clase_2"] = mixer.blend(GrupoDeClase)

            self.initial_db["espacio_clase_1"] = mixer.blend(EspacioClase)
            self.initial_db["espacio_clase_2"] = mixer.blend(EspacioClase)

            self.initial_db["clase_1"] = mixer.blend(Clase, id="101", grupo_clases=self.initial_db["grupo_clase_1"], espacio_asignado=self.initial_db["espacio_clase_1"], curso=self.initial_db["curso_1"], docente=self.initial_db["docente_1"])
            self.initial_db["clase_2"] = mixer.blend(Clase, id="102",grupo_clases=self.initial_db["grupo_clase_2"], espacio_asignado=self.initial_db["espacio_clase_2"], curso=self.initial_db["curso_1"], docente=self.initial_db["docente_1"])
    def setup_viaticos(self):
        self.setup_docentes()
        self.initial_db["materia_1"] = mixer.blend(Materia, creditos=1)
        self.initial_db["periodo_1"] = mixer.blend(Periodo, semestre="20211")
        self.setup_clases2()
        self.initial_db["viatico_1"] = mixer.blend(SolicitudViatico, clase=self.initial_db["clase_1"],tiquete=True,hospedaje=True, alimentacion=True)
        self.initial_db["viatico_2"] = mixer.blend(SolicitudViatico, clase=self.initial_db["clase_2"],tiquete=False,hospedaje=False, alimentacion=True)

    def setup_materias3(self):
        self.initial_db["departamento_1"] = mixer.blend(Departamento)
        self.initial_db["departamento_2"] = mixer.blend(Departamento)
        self.initial_db["departamento_3"] = mixer.blend(Departamento)
        self.initial_db["departamento_4"] = mixer.blend(Departamento)
        
        self.initial_db["materia_1"] = mixer.blend(Materia, creditos=1)
        self.initial_db["materia_2"] = mixer.blend(Materia, creditos=2)
        self.initial_db["materia_3"] = mixer.blend(Materia, creditos=2)
        self.initial_db["materia_4"] = mixer.blend(Materia, creditos=1)

        self.initial_db["periodo_1"] = mixer.blend(Periodo, semestre="2021-1")
        self.initial_db["periodo_2"] = mixer.blend(Periodo, semestre="2021-2")

        self.initial_db["programa_3"] = mixer.blend(Programa)

        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_1"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_2"], periodo=self.initial_db["periodo_1"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_3"], periodo=self.initial_db["periodo_1"], semestre=2)

        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_2"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_1"], materia=self.initial_db["materia_2"], periodo=self.initial_db["periodo_2"], semestre=2)

        mixer.blend(MallaCurricular, programa=self.initial_db["programa_2"], materia=self.initial_db["materia_1"], periodo=self.initial_db["periodo_1"], semestre=1)
        mixer.blend(MallaCurricular, programa=self.initial_db["programa_2"], materia=self.initial_db["materia_2"], periodo=self.initial_db["periodo_1"], semestre=1)