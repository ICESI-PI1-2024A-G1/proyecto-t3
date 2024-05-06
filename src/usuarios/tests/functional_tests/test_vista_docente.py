from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from usuarios.tests.functional_tests.base import BaseTestCase


class TestVistaDocente(BaseTestCase):

    # Botones y elementos de la página
    select_periodo = PageElement(By.ID, "periodo")

    def setUp(self):
        """
        Configura el entorno de prueba configurando los datos necesarios,
        creando un usuario e iniciando sesión.
        """
        self.setup_data3()
        self.create_user()
        self.login()

    def test_ver_basico_docente_con_clases(self):
        self.como_lider()

        periodo = self.initial_db["periodo_1"].semestre
        cedula= self.initial_db["docente_1"].cedula

        self.selenium.get(self.live_server_url + f"/usuarios/docentes/{cedula}/{periodo}")
        self.wait_for_element(By.ID, "periodo")
        self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].cedula, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].telefono, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].contrato_codigo.tipo_contrato.tipo, self.selenium.page_source)
        self.assertIn(periodo, self.selenium.page_source)
        self.assertIn(self.initial_db["clase_1"].curso.materia.nombre, self.selenium.page_source)
        

    def test_ver_basico_docente_sin_clases(self):
        self.como_lider()

        periodo = self.initial_db["periodo_2"].semestre
        cedula= self.initial_db["docente_1"].cedula

        self.selenium.get(self.live_server_url + f"/usuarios/docentes/{cedula}/{periodo}")
        self.wait_for_element(By.ID, "periodo")
        self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].cedula, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].telefono, self.selenium.page_source)
        self.assertIn(self.initial_db["docente_1"].contrato_codigo.tipo_contrato.tipo, self.selenium.page_source)
        self.assertIn(periodo, self.selenium.page_source)
        self.assertIn("No hay clases programados para este periodo", self.selenium.page_source)

    def test_docente_con_periodo_erroneo(self):
        self.como_lider()

        cedula= self.initial_db["docente_1"].cedula

        self.selenium.get(self.live_server_url + f"/usuarios/docentes/{cedula}/20235")
        self.assertIn("404", self.selenium.title)
        self.assertIn("404", self.selenium.page_source)
    
    def test_docente_con_cedula_erroneo(self):
        self.como_lider()

        periodo = self.initial_db["periodo_2"].semestre

        self.selenium.get(self.live_server_url + f"/usuarios/docentes/99999/{periodo}")
        self.assertIn("404", self.selenium.title)
        self.assertIn("404", self.selenium.page_source)

        
    