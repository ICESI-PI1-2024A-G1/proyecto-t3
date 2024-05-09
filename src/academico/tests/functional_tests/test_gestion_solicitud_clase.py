from datetime import datetime
from unittest import skipUnless
import time

from django.conf import settings
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from academico.models import (Clase, Curso, Departamento, Director, Docente,
                              Espacio, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Modalidad, Periodo,
                              Programa, TipoDeMateria, TipoDePrograma, EspacioClase)
from academico.views import crear_clase, eliminar_clase
from usuarios.models import Ciudad, Persona, Usuario, Contrato, EstadoDocente, TipoContrato, EstadoContrato
from usuarios.tests.functional_tests.base import BaseTestCase


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class LoginPageTestCase(BaseTestCase):

    grupos = PageElement(By.ID, "Materias posgrado btn")

    def setUp(self):

        self.user = User.objects.create_user("user", "user@example.com", "user")
        grupo = mixer.blend("auth.Group", name="lider")
        self.user.groups.add(grupo)
        self.user.save()
        
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)

        self.user2 = User.objects.create_user("user2", "user2@example.com", "user2")
        grupo = mixer.blend("auth.Group", name="banner")
        self.user2.groups.add(grupo)
        self.user2.save()
        
        persona2 = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona2, usuario=self.user2)


        cali = Ciudad.objects.create(ciudad="Cali")
        facultadA = Facultad.objects.create(nombre="Facultad A")
        director = Director.objects.create(
        cedula="123456",
        nombre="juan",
        email="juan@gmail.com",
        telefono="123456",
        ciudad=cali,
        fechaNacimiento="2021-01-01",
        oficina="oficina",
        )
        aprobado = EstadoSolicitud.objects.create(nombre="Aprobado")
        maestria = TipoDePrograma.objects.create(nombre="Maestria")
        programa = Programa.objects.create(
        codigo="P1",
        nombre="Programa 1",
        facultad=facultadA,
        director=director,
        estado_solicitud=aprobado,
        tipo_de_programa=maestria,
        )

        
        periodo = Periodo.objects.create(semestre='202401', fecha_inicio=datetime.now(), fecha_fin=datetime.now())
        departamento = Departamento.objects.create(codigo=1, nombre="Departamento 1")
        tipo_materia = TipoDeMateria.objects.create(tipo="1")
        materia = Materia.objects.create(codigo=1, nombre="Materia", creditos=3, departamento=departamento, tipo_de_materia=tipo_materia)
        

        curso = Curso.objects.create(grupo = '4', cupo = 10, materia_id=materia.codigo, periodo_id=periodo.semestre)
        curso = Curso.objects.create(grupo = '5', cupo = 10, materia_id=materia.codigo, periodo_id=periodo.semestre)
        curso = Curso.objects.create(grupo = '6', cupo = 10, materia_id=materia.codigo, periodo_id=periodo.semestre)

        tipo_espacio = Espacio.objects.create(id=1,tipo="Salon", capacidad="200")
        tipo_espacio = Espacio.objects.create(id=2,tipo="Salon", capacidad="30")
        tipo_espacio = Espacio.objects.create(id=3,tipo="Salon", capacidad="200")
        tipo_espacio = Espacio.objects.create(id=4,tipo="Salon", capacidad="5")

        espacio_clase = EspacioClase.objects.create(edificio = "D", numero = 101, tipo_id=1)

        modalidad = Modalidad.objects.create(id=1, metodologia="Presencial")
        modalidad = Modalidad.objects.create(id=3, metodologia="Presencial")
        modalidad = Modalidad.objects.create(id=4, metodologia="Presencial")




        ciudad = Ciudad.objects.create(id =100, ciudad="Boyaca")
        estado_docente = EstadoDocente.objects.create(id=1, estado="Activo")
        tipo_contrato = TipoContrato.objects.create(id=1, tipo="Contrato de prestación de servicios")
        estado_contrato = EstadoContrato.objects.create(id=1, estado="Activo")
        contrato = Contrato.objects.create(codigo="1", fecha_elaboracion="2023-01-01", tipo_contrato=tipo_contrato, estado=estado_contrato)

        docente = Docente.objects.create(cedula="1", nombre="juan", email="a",  telefono="1", ciudad=ciudad, fechaNacimiento="2021-01-01", contrato_codigo=contrato, estado=estado_docente, foto="a")




    
    def test_gestion_solicitud_clase_1(self):
    # Iniciar sesión primero
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_lider()


        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias')
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()
        

        curso = self.selenium.find_element(By.ID, "49")
        curso.click()

        self.selenium.find_element(By.CSS_SELECTOR, "a[onclick=\"show()\"]").click()
        
        self.selenium.find_element(By.NAME, "start_day").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "start_day").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "start_day").send_keys("1600PM")
        self.selenium.find_element(By.NAME, "end_day").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "end_day").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "end_day").send_keys("1800PM")
        self.selenium.find_element(By.NAME, "tipo_espacio").send_keys(1)
        self.selenium.find_element(By.NAME, "modalidad_clase").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase").send_keys("juan")
        self.selenium.find_element(By.NAME, "num_semanas").send_keys(16)

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()

        # Encuentra todos los checkboxes que comienzan con "check-grupo"
        checkboxes = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=check-grupo]")



        # Haz clic en el primer checkbox
        checkboxes[0].click()




        # Encuentra el botón con un atributo 'onclick' que es 'Solicitud_Salones()'
        boton_solicitud = self.selenium.find_element(By.XPATH, "//*[@onclick='Solicitud_Salones()']")

        # Haz clic en el botón
        boton_solicitud.click()

        # Espera hasta que la alerta esté presente
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())

        # Cambia a la alerta y haz clic en "Aceptar"
        alert = self.selenium.switch_to.alert
        alert.accept()
        boton_cerrar_sesion = self.selenium.find_element(By.ID, "logout-btn")

        # Haz clic en el botón de cerrar sesión
        boton_cerrar_sesion.click()

        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user2")
        self.selenium.find_element(By.NAME, "password").send_keys("user2")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_banner()



        

        # Encuentra el menú desplegable por su nombre
        menu_desplegable = Select(self.selenium.find_element(By.NAME, "espacio_asignado"))

        # Selecciona una opción por su valor
        # Reemplaza 'valor' con el valor de la opción que quieres seleccionar
        menu_desplegable.select_by_value("1")



        # Encuentra el botón con un atributo 'onclick' que es 'Solicitud_Salones()'
        boton_aceptar = self.selenium.find_element(By.XPATH, "//*[@onclick='Solicitud_Salones()']")

        # Haz clic en el botón
        boton_aceptar.click()
        time.sleep(5)

        self.assertIn("Server Error (500)", self.selenium.page_source)

