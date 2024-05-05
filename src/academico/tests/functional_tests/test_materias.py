from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from usuarios.models import Persona, Usuario, Ciudad
from academico.models import Programa, Periodo, Materia, Departamento, TipoDeMateria, Director, EstadoSolicitud, Facultad, TipoDePrograma, MallaCurricular


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class MateriasTestCase(SeleniumTestCase):

    username = PageElement(By.ID, "username")
    password = PageElement(By.ID, "password")
    submit = PageElement(By.ID, "submit")
    logout = PageElement(By.ID, "logout-btn")
    lista_materias = PageElement(By.ID, "Materias posgrado btn")
    search = PageElement(By.ID, "search-form")
    filtro_submit = PageElement(By.ID, "filtrar_materias")

    def setUp(self):
        self.user = User.objects.create_user("user", "user@example.com", "user")
        grupo = mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(grupo)
        self.user.save()
        
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)
        
        self.departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
        self.departamento2 = Departamento.objects.create(codigo=2, nombre="Departamento 2")
        self.tipo_materia = TipoDeMateria.objects.create(tipo="1")
        self.periodo = Periodo.objects.create(semestre="202101", fecha_inicio="2021-01-01", fecha_fin="2021-06-30")
        
        self.cali = Ciudad.objects.create(ciudad="Cali")
        self.facultadA = Facultad.objects.create(nombre="Facultad A")
        self.director = Director.objects.create(
            cedula="123456",
            nombre="juan",
            email="juan@gmail.com",
            telefono="123456",
            ciudad=self.cali,
            fechaNacimiento="2021-01-01",
            oficina="oficina",
        )
        self.aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
        self.maestria = TipoDePrograma.objects.create(nombre="Maestria")
        self.programa = Programa.objects.create(
            codigo="P1",
            nombre="Programa 1",
            facultad=self.facultadA,
            director=self.director,
            estado_solicitud=self.aprobado,
            tipo_de_programa=self.maestria,
        )
        
        self.materia = Materia.objects.create(codigo=1, nombre="Materia 1", creditos=3, departamento=self.departamento, tipo_de_materia=self.tipo_materia)
        self.materia2 = Materia.objects.create(codigo=2, nombre="Materia 2", creditos=4, departamento=self.departamento2, tipo_de_materia=self.tipo_materia)
        
        MallaCurricular.objects.create(materia = self.materia, programa = self.programa, periodo = self.periodo, semestre="202101")
        MallaCurricular.objects.create(materia = self.materia2, programa = self.programa, periodo = self.periodo, semestre="202101")
        
        

        

    def test_filtrado_positivo_valido(self):
        # Visitar la página
        self.selenium.get(self.live_server_url)

        # Llenar el formulario y enviar
        self.username.send_keys("user")
        self.password.send_keys("user")
        self.submit.click()
        
        # Buscar listado de sidebar
        self.lista_materias.click()
        
        #Llenar form para filrado
        self.search.send_keys("Departamento 1")
        
        # Press Enter key
        self.search.send_keys(Keys.ENTER)

        # Validar que se redirigió a la página de inicio
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/materias?q=Ingeniería"
        )
        self.assertNotIn("Departamento 2", self.selenium.page_source)

