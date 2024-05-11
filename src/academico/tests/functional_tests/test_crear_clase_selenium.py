from datetime import datetime
import time
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




    
    def test_crear_clase_1(self):
        """
    Prueba la creación de una clase en la aplicación.

    Esta prueba sigue los siguientes pasos:

    1. Inicia sesión en la aplicación con el nombre de usuario y la contraseña "user".
    2. Navega a la página de materias.
    3. Selecciona la primera materia de la lista.
    4. Selecciona el curso con el NRC correspondiente.
    5. Abre el formulario de creación de clase.
    6. Rellena el formulario con los siguientes datos:
        - Fecha y hora de inicio: 02/20/2024 a las 16:00 PM
        - Fecha y hora de fin: 02/20/2024 a las 18:00 PM
        - Tipo de espacio: 1
        - Modalidad de clase: 1
        - Docente de clase: "juan"
    7. Hace clic en el botón de envío para crear la clase.
    8. Verifica que la URL actual es la página del curso.
    9. Verifica que "Clase 1" está presente en el código fuente de la página, lo que indica que la clase se creó correctamente.

    Si todos estos pasos se completan sin errores, la prueba pasará.
    """
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

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Clase 1", self.selenium.page_source)


    def test_crear_clase_2(self):
        """
    Prueba la creación de una segunda clase en la aplicación.

    Descripcion: Esta prueba varia en parametros de una clase y da un resultado positivo en creacion
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

        

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Modulo de clases 1", self.selenium.page_source)
        
    

    
    def test_crear_clase_3(self):
        """
        Prueba la creación de una tercera clase en la aplicación.
        Descripcion: Esta prueba varia en parametros de una clase y da un resultado positivo en creacion
        
        """

        self.selenium.get(self.live_server_url + '/login')
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

        self.selenium.find_element(By.NAME, "tipo_espacio").send_keys(3)

        self.selenium.find_element(By.NAME, "modalidad_clase").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase").send_keys("")
        self.selenium.find_element(By.NAME, "num_semanas").send_keys(16)

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Clase 1", "Clase 16", self.selenium.page_source)
    
    
    def test_crear_clase_4(self):
        """
        Prueba la creación de una quinta clase en la aplicación.

        Esta prueba tiene un diseño preeliminar variando ciertos datos, pero en este caso, el docente de la clase es "juan".

        Si todos estos pasos se completan sin errores, la prueba pasará.
        """
        self.selenium.get(self.live_server_url + '/login')
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

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Clase 1", self.selenium.page_source)

    
    def test_crear_clase_5(self):
        """
        Prueba la creación de una quinta clase en la aplicación.

        Esta prueba sigue los mismos pasos que la prueba 4, pero en este caso, el docente de la clase es "juan".

        Si todos estos pasos se completan sin errores, la prueba pasará.
        """
        self.selenium.get(self.live_server_url + '/login')
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

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Clase 1", self.selenium.page_source)

    
    def test_crear_clase_6(self):
        """
        Prueba la creación de una sexta clase en la aplicación.

        Esta prueba sigue los mismos pasos que la prueba 5, pero en este caso, el campo del docente de la clase se deja vacío.

        Si todos estos pasos se completan sin errores, la prueba pasará.
        """
        self.selenium.get(self.live_server_url + '/login')
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
        self.selenium.find_element(By.NAME, "docente_clase").send_keys("")

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("Clase 1", self.selenium.page_source)
    
    
    def test_crear_clase_7(self):
        """
        Prueba la creación de una séptima clase en la aplicación.

        Esta prueba sigue los mismos pasos que la prueba 6, pero en este caso, la hora de finalización de la clase es anterior a la hora de inicio. Se espera que la aplicación muestre un mensaje de error indicando que la hora de inicio no puede ser posterior a la hora de finalización.

        Si todos estos pasos se completan sin errores, la prueba pasará.
        """
        self.selenium.get(self.live_server_url + '/login')
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
        self.selenium.find_element(By.NAME, "end_day").send_keys("1500PM")

        self.selenium.find_element(By.NAME, "tipo_espacio").send_keys(1)

        self.selenium.find_element(By.NAME, "modalidad_clase").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase").send_keys("juan")

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("La fecha/hora de inicio no puede ser posterior a la fecha/hora de finalización.", self.selenium.page_source)

    
    def test_crear_clase_8(self):
        """
        Prueba la creación de una octava clase en la aplicación.

        Esta prueba sigue los mismos pasos que la prueba 7, pero en este caso, la duración de la clase es mayor a 24 horas. Se espera que la aplicación muestre un mensaje de error indicando que la duración de la clase no puede ser mayor a 24 horas.

        Si todos estos pasos se completan sin errores, la prueba pasará.
        """ 
        self.selenium.get(self.live_server_url + '/login')
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

        self.selenium.find_element(By.NAME, "start_day").send_keys("1/02/2024")
        self.selenium.find_element(By.NAME, "start_day").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "start_day").send_keys("1600PM")

        self.selenium.find_element(By.NAME, "end_day").send_keys("3/02/024")
        self.selenium.find_element(By.NAME, "end_day").send_keys(Keys.TAB)
        self.selenium.find_element(By.NAME, "end_day").send_keys("1800PM")

        self.selenium.find_element(By.NAME, "tipo_espacio").send_keys(1)

        self.selenium.find_element(By.NAME, "modalidad_clase").send_keys(1)
        self.selenium.find_element(By.NAME, "docente_clase").send_keys("")

        # Hacer clic en el botón de envío
        self.selenium.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
        time.sleep(5)

        self.assertEqual(
            self.selenium.current_url, self.live_server_url + f"/academico/cursos/{self.curso.nrc}"
        )
        self.assertIn("La duración de la clase no puede ser mayor a 24 horas", self.selenium.page_source)    
    




    