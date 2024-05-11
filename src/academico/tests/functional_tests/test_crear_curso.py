from datetime import datetime
from unittest import skipUnless

from django.conf import settings
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django_selenium_test import PageElement, SeleniumTestCase
from mixer.backend.django import mixer
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time 

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
    submit = PageElement(By.CLASS_NAME, "btn btn-primary mt-2")
    

    def setUp(self):
        """
        Configura el entorno de prueba creando datos necesarios, un usuario y realizando el inicio de sesión.
        """
        self.setup_data5()
        self.create_user()
        self.login()



    def test_crear_curso_2(self):
        self.como_lider()

            # Navegar a la página de creación de clase
        self.selenium.get(self.live_server_url + '/academico/materias/' + str(self.initial_db["materia_1"].codigo) + '/'+self.initial_db["periodo_1"].semestre)
        time.sleep(100)
        
        self.submit.click()
        cupos = PageElement(By.ID, "cantidad_de_cupos")
        cupos.click()
        cupos.send_keys(1)
        submit2 = PageElement(By.VALUE, "Crear curso")
        submit2.click()
        time.sleep(100)



        


        
           


