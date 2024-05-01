from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from usuarios.tests.functional_tests.base import BaseTestCase


class TestGestionPrograma(BaseTestCase):

    # Botones y elementos de la página
    select_periodo = PageElement(By.ID, "periodo")

    def setUp(self):
        """
        Configura el entorno de prueba configurando los datos necesarios,
        creando un usuario e iniciando sesión.
        """
        self.setup_data()
        self.create_user()
        self.login()

    def asserts_basicos_programa_1(self, periodo):
        """
        Este método realiza las afirmaciones básicas para el objeto programa_1 en la interfaz de usuario.

        Args:
            periodo (str): El período del semestre.

        Returns:
            None
        """
        self.assertIn(self.initial_db["programa_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["programa_1"].codigo, self.selenium.page_source)
        self.assertIn(self.initial_db["programa_1"].facultad.nombre, self.selenium.page_source)

        self.assertIn(self.initial_db["director_1"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["director_1"].email, self.selenium.page_source)
        self.assertIn(self.initial_db["director_1"].telefono, self.selenium.page_source)

        if periodo == self.initial_db["periodo_1"].semestre:
            self.assertIn("Créditos totales:</strong> 5</label>", self.selenium.page_source)
            self.assertIn("Cursos totales:</strong> 3</label>", self.selenium.page_source)

            self.assertNotIn("No hay docentes asignados a este programa", self.selenium.page_source)
            self.assertIn(self.initial_db["docente_1"].nombre, self.selenium.page_source)

            self.assertIn("1°", self.selenium.page_source)
            self.assertIn("2°", self.selenium.page_source)

            self.assertIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
            self.assertIn(self.initial_db["materia_2"].nombre, self.selenium.page_source)
            self.assertIn(self.initial_db["materia_3"].nombre, self.selenium.page_source)

        if periodo == self.initial_db["periodo_2"].semestre:
            self.assertIn("Créditos totales:</strong> 3</label>", self.selenium.page_source)
            self.assertIn("Cursos totales:</strong> 2</label>", self.selenium.page_source)

            self.assertIn("No hay docentes asignados a este programa", self.selenium.page_source)

            self.assertIn(self.initial_db["materia_1"].nombre, self.selenium.page_source)
            self.assertIn(self.initial_db["materia_2"].nombre, self.selenium.page_source)

    def asserts_basicos_programa_2(self, periodo):
        """
        Realiza las aserciones básicas para el objeto programa_2 en la prueba funcional.

        Args:
            periodo (str): El semestre del programa.
        """
        self.assertIn(self.initial_db["programa_2"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["programa_2"].codigo, self.selenium.page_source)
        self.assertIn(self.initial_db["programa_2"].facultad.nombre, self.selenium.page_source)

        self.assertIn(self.initial_db["director_2"].nombre, self.selenium.page_source)
        self.assertIn(self.initial_db["director_2"].email, self.selenium.page_source)
        self.assertIn(self.initial_db["director_2"].telefono, self.selenium.page_source)

        if periodo == self.initial_db["periodo_1"].semestre:
            self.assertIn("Créditos totales:</strong> 3</label>", self.selenium.page_source)
            self.assertIn("Cursos totales:</strong> 2</label>", self.selenium.page_source)

    def test_ver_como_lider(self):
        """
        Prueba funcional para verificar la visualización de un programa académico como líder.
        
        Debe mostrar la información básica del programa, los botones de enviar para revisión,
        importar malla y editar.
        
        No debe mostrar el estado del programa del director, ni los botones de aprobar programa.
        
        Returns:
            None
        """
        self.como_lider() # Cambiar a rol de líder

        # Variables a utilizar
        codigo = self.initial_db["programa_1"].codigo
        semestre = self.initial_db["periodo_1"].semestre

        self.selenium.get(self.live_server_url + f"/academico/programas/{codigo}/{semestre}")

        # Validar programa
        self.asserts_basicos_programa_1(semestre)
        self.assertIn("Enviar para revisión", self.selenium.page_source) # Debe aparecer el botón de enviar para revisión
        self.assertIn("Importar malla", self.selenium.page_source) # Debe aparecer el botón de importar malla
        self.assertIn("btn-editar", self.selenium.page_source) # Debe aparecer el botón de editar

    def test_ver_como_director(self):
        """
        Prueba funcional para verificar la visualización de un programa académico como director.
        
        Debe mostrar la información básica del programa, el estado del programa del director,
        y no debe mostrar los botones de enviar para revisión, importar malla y editar.
        
        Returns:
            None
        """
        self.como_director() # Cambiar a rol de director

        # Variables a utilizar
        codigo = self.initial_db["programa_1"].codigo
        semestre = self.initial_db["periodo_1"].semestre

        self.selenium.get(self.live_server_url + f"/academico/programas/{codigo}/{semestre}")

        # Validar programa
        self.asserts_basicos_programa_1(semestre)
        self.assertIn("Programa En espera", self.selenium.page_source) # Debe aparecer el estado del programa del director
        self.assertNotIn("Importar malla", self.selenium.page_source) # No debe aparecer el botón de importar malla
        self.assertNotIn("btn-editar", self.selenium.page_source) # No debe aparecer el botón de editar

    def test_ver_como_gestor(self):
        """
        Prueba funcional para verificar la visualización de un programa académico como gestor.
        
        Debe mostrar la información básica del programa, y no debe mostrar los botones de enviar para revisión,
        importar malla y editar.
        
        Returns:
            None
        """
        self.como_gestor() # Cambiar a rol de gestor

        # Variables a utilizar
        codigo = self.initial_db["programa_1"].codigo
        semestre = self.initial_db["periodo_1"].semestre

        self.selenium.get(self.live_server_url + f"/academico/programas/{codigo}/{semestre}")

        # Validar programa
        self.asserts_basicos_programa_1(semestre)
        self.assertNotIn("Programa En espera", self.selenium.page_source) # No debe aparecer el estado del programa del director
        self.assertNotIn("Enviar para revisión", self.selenium.page_source) # No debe aparecer el botón de enviar para revisión
        self.assertNotIn("Importar malla", self.selenium.page_source) # No debe aparecer el botón de importar malla
        self.assertNotIn("btn-editar", self.selenium.page_source) # No debe aparecer el botón de editar

    def test_navegar_entre_periodos(self):
        """
        Prueba funcional para verificar la navegación entre periodos de un programa académico.
        
        Debe permitir cambiar entre periodos y mostrar la información correspondiente a cada periodo.
        
        Returns:
            None
        """
        self.como_lider()

        # Variables a utilizar
        codigo = self.initial_db["programa_1"].codigo
        semestre_1 = self.initial_db["periodo_1"].semestre
        semestre_2 = self.initial_db["periodo_2"].semestre

        self.selenium.get(self.live_server_url + f"/academico/programas/{codigo}/{semestre_1}")

        # Verificar que se cargue correctamente el primer periodo
        self.asserts_basicos_programa_1(semestre_1)

        # Cambiar a otro periodo
        Select(self.select_periodo).select_by_value(f"{codigo}/{semestre_2}")

        # Verificar que se cargue correctamente el nuevo periodo
        self.asserts_basicos_programa_1(semestre_2)

    def test_distintos_programas(self):
        """
        Prueba funcional para verificar la visualización de distintos programas académicos.
        
        Debe mostrar la información básica de cada programa, y los botones de enviar para revisión,
        importar malla y editar.
        
        Returns:
            None
        """
        self.como_lider()

        # Variables a utilizar
        codigo_1 = self.initial_db["programa_1"].codigo
        codigo_2 = self.initial_db["programa_2"].codigo
        semestre = self.initial_db["periodo_1"].semestre

        self.selenium.get(self.live_server_url + f"/academico/programas/{codigo_1}/{semestre}")

        # Validar programa 1
        self.asserts_basicos_programa_1(semestre)
        self.assertIn("Enviar para revisión", self.selenium.page_source) # Debe aparecer el botón de enviar para revisión
        self.assertIn("Importar malla", self.selenium.page_source) # Debe aparecer el botón de importar malla
        self.assertIn("btn-editar", self.selenium.page_source) # Debe aparecer el botón de editar

        self.selenium.get(self.live_server_url + f"/academico/programas/{codigo_2}/{semestre}")

        # Validar programa 2
        self.asserts_basicos_programa_2(semestre)
        self.assertIn("Enviar para revisión", self.selenium.page_source) # Debe aparecer el botón de enviar para revisión
        self.assertIn("Importar malla", self.selenium.page_source) # Debe aparecer el botón de importar malla
        self.assertIn("btn-editar", self.selenium.page_source) # Debe aparecer el botón de editar
