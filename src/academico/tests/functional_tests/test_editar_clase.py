import time
from datetime import datetime
from unittest import skipUnless

from django.conf import settings
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from academico.models import (Clase, Curso, Departamento, Director, Docente,
                              Espacio, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Modalidad, Periodo,
                              Programa, TipoDeMateria, TipoDePrograma)
from academico.views import crear_clase, eliminar_clase
from usuarios.models import (Ciudad, Contrato, EstadoContrato, EstadoDocente,
                             Persona, TipoContrato, Usuario)
from usuarios.tests.functional_tests.base import BaseTestCase


@skipUnless(getattr(settings, "SELENIUM_WEBDRIVERS", False), "Selenium is unconfigured")
class LoginPageTestCase(BaseTestCase):

    grupos = PageElement(By.ID, "Materias posgrado btn")

    def setUp(self):
        """
        Método de configuración para las pruebas.

        Este método se ejecuta antes de cada prueba y se utiliza para configurar cualquier estado o datos necesarios para las pruebas.

        En este método, se crean varios objetos en la base de datos que se utilizan en las pruebas. Estos incluyen:

        - Un usuario con el nombre de usuario "user" y la contraseña "user", que es miembro del grupo "gestores".
        - Una persona y un usuario asociado a esa persona.
        - Una ciudad llamada "Cali".
        - Una facultad llamada "Facultad A".
        - Un director llamado "juan".
        - Un estado de solicitud llamado "Aprobado".
        - Un tipo de programa llamado "Maestria".
        - Un programa con el código "P1" y el nombre "Programa 1".
        - Un periodo con el semestre '202401' y fechas de inicio y fin actuales.
        - Un departamento con el código 1 y el nombre "Departamento 1".
        - Un tipo de materia con el tipo "1".
        - Una materia con el código 1, el nombre "Materia" y 3 créditos.
        - Tres cursos con los grupos '4', '5' y '6', todos con un cupo de 10 y asociados a la materia y el periodo creados anteriormente.
        - Cuatro espacios de tipo "Salon" con capacidades de "200", "30", "200" y "5".
        - Tres modalidades con la metodología "Presencial".
        - Una ciudad con el id 100 y el nombre "Boyaca".
        - Un estado de docente llamado "Activo".
        - Un tipo de contrato llamado "Contrato de prestación de servicios".
        - Un estado de contrato llamado "Activo".
        - Un contrato con el código "1" y la fecha de elaboración "2023-01-01".
        - Un docente llamado "juan".
        """

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

        self.curso = Curso.objects.create(grupo = '4', cupo = 10, materia_id=materia.codigo, periodo_id=periodo.semestre)
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

        """
        Test para editar una clase.

        Se crea una clase para posteriormente editarla y que se guarden los cambios pertinentes
        """
        # Iniciar sesión primero
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_lider()

        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + "/academico/materias")
        self.wait_for_element(By.CSS_SELECTOR, "tbody tr")
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()

        self.wait_for_element(By.ID, self.curso.nrc)
        curso = self.selenium.find_element(By.ID, self.curso.nrc)
        curso.click()

        self.wait_for_element(By.CSS_SELECTOR, 'a[onclick="show()"]')
        self.selenium.find_element(By.CSS_SELECTOR, 'a[onclick="show()"]').click()

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

        self.wait_for_element(By.CSS_SELECTOR, "[id^=class_group]")
        modulos = self.selenium.find_elements(By.CSS_SELECTOR, "[id^=class_group]")
        modulos[0].click()
        dropdown_button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "dropdownMenuButton"))
        )
        dropdown_button.click()
        time.sleep(2)
        # Espera hasta que el enlace de editar esté presente y haz clic en él
        editar_link = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Editar"))
        )
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
        actualizar_clase_button = WebDriverWait(self.selenium, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Actualizar Clase')]")
            )
        )
        actualizar_clase_button.click()

        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url + f"/academico/cursos/{self.curso.nrc}",
        )
        self.assertIn("Clase 1", self.selenium.page_source)

    def test_editar_clase_2(self):

        """
        Test para editar una clase.

        Se crea una clase para posteriormente editarla y que se guarden los cambios pertinentes
        Se cambia dato donde se crea una clase con un docente y posteriormente se edita para que no tenga docente
        """
        # Iniciar sesión primero
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_lider()

        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias')
        self.wait_for_element(By.CSS_SELECTOR, "tbody tr")
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()

        self.wait_for_element(By.ID, self.curso.nrc)
        curso = self.selenium.find_element(By.ID, self.curso.nrc)
        curso.click()

        self.wait_for_element(By.CSS_SELECTOR, "a[onclick=\"show()\"]")
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

        self.wait_for_element(By.CSS_SELECTOR, "[id^=class_group]")
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
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Sin asignar", self.selenium.page_source)

    def test_editar_clase_3(self):

        """
        Test para editar una clase.

        Se crea una clase para posteriormente editarla y que se guarden los cambios pertinentes
        """
        # Iniciar sesión primero
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_lider()

        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias')
        self.wait_for_element(By.CSS_SELECTOR, "tbody tr")
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()

        self.wait_for_element(By.ID, self.curso.nrc)
        curso = self.selenium.find_element(By.ID, self.curso.nrc)
        curso.click()

        self.wait_for_element(By.CSS_SELECTOR, "a[onclick=\"show()\"]")
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

        self.wait_for_element(By.CSS_SELECTOR, "[id^=class_group]")
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
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("juan", self.selenium.page_source)

    def test_editar_clase_4(self):
        """
        Test para editar una clase.

        Se crea una clase para posteriormente editarla y que se guarden los cambios pertinentes

        Esta prueba va guiada a comprobar las validaciones a la hora de editar una clase a un dato incorrecto

        En este caso no se puede guardar una clae en la que la fecha de inicio sea posterior a la fecha de finalización
        """
        # Iniciar sesión primero
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_lider()

        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias')
        self.wait_for_element(By.CSS_SELECTOR, "tbody tr")
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()

        self.wait_for_element(By.ID, self.curso.nrc)
        curso = self.selenium.find_element(By.ID, self.curso.nrc)
        curso.click()

        self.wait_for_element(By.CSS_SELECTOR, "a[onclick=\"show()\"]")
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

        self.wait_for_element(By.CSS_SELECTOR, "[id^=class_group]")
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

        """
        Test para editar una clase.

        Se crea una clase para posteriormente editarla y que se guarden los cambios pertinentes

        Esta prueba va guiada a comprobar las validaciones a la hora de editar una clase a un dato incorrecto

        En este caso corroborar que a la hora de editar la clase, una clase no pueda ser mayor a 24 horas
        """
        # Iniciar sesión primero
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.NAME, "username").send_keys("user")
        self.selenium.find_element(By.NAME, "password").send_keys("user")
        self.selenium.find_element(By.ID, "submit").click()
        self.como_lider()

        # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias')
        self.wait_for_element(By.CSS_SELECTOR, "tbody tr")
        materias = self.selenium.find_elements(By.CSS_SELECTOR, "tbody tr")
        materias[0].click()

        self.wait_for_element(By.ID, self.curso.nrc)
        curso = self.selenium.find_element(By.ID, self.curso.nrc)
        curso.click()

        self.wait_for_element(By.CSS_SELECTOR, "a[onclick=\"show()\"]")
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

        self.wait_for_element(By.CSS_SELECTOR, "[id^=class_group]")
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
