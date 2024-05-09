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

from academico.models import (Clase, Curso, Departamento, Director, Docente,
                              Espacio, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Modalidad, Periodo,
                              Programa, TipoDeMateria, TipoDePrograma)
from academico.views import crear_clase, eliminar_clase
from usuarios.models import Ciudad, Persona, Usuario, Contrato, EstadoDocente, TipoContrato, EstadoContrato
from usuarios.tests.functional_tests.base import BaseTestCase


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class LoginPageTestCase(BaseTestCase):

    grupos = PageElement(By.ID, "Materias posgrado btn")

    def setUp(self):

        self.user = User.objects.create_user("user", "user@example.com", "user")
        grupo = mixer.blend("auth.Group", name="gestores")
        self.user.groups.add(grupo)
        self.user.save()
        
        persona = mixer.blend(Persona)
        mixer.blend(Usuario, persona=persona, usuario=self.user)


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

        modalidad = Modalidad.objects.create(id=1, metodologia="Presencial")
        modalidad = Modalidad.objects.create(id=3, metodologia="Presencial")
        modalidad = Modalidad.objects.create(id=4, metodologia="Presencial")


        ciudad = Ciudad.objects.create(id =100, ciudad="Boyaca")
        estado_docente = EstadoDocente.objects.create(id=1, estado="Activo")
        tipo_contrato = TipoContrato.objects.create(id=1, tipo="Contrato de prestación de servicios")
        estado_contrato = EstadoContrato.objects.create(id=1, estado="Activo")
        contrato = Contrato.objects.create(codigo="1", fecha_elaboracion="2023-01-01", tipo_contrato=tipo_contrato, estado=estado_contrato)

        docente = Docente.objects.create(cedula="1", nombre="juan", email="a",  telefono="1", ciudad=ciudad, fechaNacimiento="2021-01-01", contrato_codigo=contrato, estado=estado_docente, foto="a")




    
    def test_editar_clase_1(self):
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
        

        curso = self.selenium.find_element(By.ID, "25")
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

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()
        dropdown_button = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "dropdownMenuButton")))
        dropdown_button.click()
        time.sleep(2)
        # Espera hasta que el enlace de editar esté presente y haz clic en él
        editar_link = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Editar")))
        editar_link.click()
        
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("1600PM")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("1800PM")
        self.selenium.find_element(By.NAME, "tipo_espacio_e").send_keys(1)
        self.selenium.find_element(By.NAME, "modalidad_clase_e").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase_e").send_keys("juan")

        # Hacer clic en el botón de envío
        # Espera hasta que el botón de "Actualizar Clase" esté presente y haz clic en él
        actualizar_clase_button = WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Actualizar Clase')]")))
        actualizar_clase_button.click()

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/cursos/25"
        )
        self.assertIn("Clase 1", self.selenium.page_source)


    def test_editar_clase_2(self):
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
        

        curso = self.selenium.find_element(By.ID, "28")
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

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()
        dropdown_button = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "dropdownMenuButton")))
        dropdown_button.click()
        time.sleep(2)
        # Espera hasta que el enlace de editar esté presente y haz clic en él
        editar_link = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Editar")))
        editar_link.click()

        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("1600PM")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("1800PM")
        self.selenium.find_element(By.NAME, "tipo_espacio_e").send_keys(1)
        self.selenium.find_element(By.NAME, "modalidad_clase_e").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase_e").send_keys("Sin asignar")

        # Hacer clic en el botón de envío
        # Espera hasta que el botón de "Actualizar Clase" esté presente y haz clic en él
        actualizar_clase_button = WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Actualizar Clase')]")))
        actualizar_clase_button.click()

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/cursos/28"
        )
        self.assertIn("Sin asignar", self.selenium.page_source)

    

    def test_editar_clase_3(self):
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
        

        curso = self.selenium.find_element(By.ID, "31")
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

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()
        dropdown_button = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "dropdownMenuButton")))
        dropdown_button.click()
        time.sleep(2)
        # Espera hasta que el enlace de editar esté presente y haz clic en él
        editar_link = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Editar")))
        editar_link.click()

        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("1600PM")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("1800PM")
        self.selenium.find_element(By.NAME, "tipo_espacio_e").send_keys(1)
        self.selenium.find_element(By.NAME, "modalidad_clase_e").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase_e").send_keys("juan")

        # Hacer clic en el botón de envío
        # Espera hasta que el botón de "Actualizar Clase" esté presente y haz clic en él
        actualizar_clase_button = WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Actualizar Clase')]")))
        actualizar_clase_button.click()

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/academico/cursos/31"
        )
        self.assertIn("juan", self.selenium.page_source)

    def test_editar_clase_4(self):
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
        

        curso = self.selenium.find_element(By.ID, "34")
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

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()
        dropdown_button = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "dropdownMenuButton")))
        dropdown_button.click()
        time.sleep(2)
        # Espera hasta que el enlace de editar esté presente y haz clic en él
        editar_link = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Editar")))
        editar_link.click()
        
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("1600PM")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("1400PM")
        self.selenium.find_element(By.NAME, "tipo_espacio_e").send_keys(1)
        self.selenium.find_element(By.NAME, "modalidad_clase_e").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase_e").send_keys("Sin asignar")

        # Hacer clic en el botón de envío
        # Espera hasta que el botón de "Actualizar Clase" esté presente y haz clic en él
        actualizar_clase_button = WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Actualizar Clase')]")))
        actualizar_clase_button.click()

        self.assertIn("La fecha/hora de inicio no puede ser posterior a la fecha/hora de finalización.", self.selenium.page_source)


    def test_editar_clase_5(self):
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
        

        curso = self.selenium.find_element(By.ID, "37")
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

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()
        dropdown_button = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "dropdownMenuButton")))
        dropdown_button.click()
        time.sleep(2)
        # Espera hasta que el enlace de editar esté presente y haz clic en él
        editar_link = WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Editar")))
        editar_link.click()
        
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_inicio").send_keys("1600PM")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("02/20/2024")
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "fecha_fin").send_keys("1800PM")
        self.selenium.find_element(By.NAME, "tipo_espacio_e").send_keys(1)
        self.selenium.find_element(By.NAME, "modalidad_clase_e").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase_e").send_keys("Sin asignar")

        # Hacer clic en el botón de envío
        # Espera hasta que el botón de "Actualizar Clase" esté presente y haz clic en él
        actualizar_clase_button = WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Actualizar Clase')]")))
        actualizar_clase_button.click()

    
        self.assertIn("La duración de la clase no puede ser mayor a 24 horas.", self.selenium.page_source)


    