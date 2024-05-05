from django_selenium_test import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from usuarios.tests.functional_tests.base import BaseTestCase


class CrearUsuarioTestCase(BaseTestCase):

    nuevo_usuario_btn = PageElement(By.CSS_SELECTOR, 'a[onclick="show()"]')
    cedula_input = PageElement(By.ID, 'cedula')
    nombre_input = PageElement(By.ID, 'nombre')
    apellido_input = PageElement(By.ID, 'apellido')
    email_input = PageElement(By.ID, 'email')
    telefono_input = PageElement(By.ID, 'telefono')
    ciudad_select = PageElement(By.ID, 'ciudad')
    birthdate_input = PageElement(By.ID, 'birthdate')
    rol_select = PageElement(By.ID, 'rol')
    crear_usuario_btn = PageElement(By.CSS_SELECTOR, 'button[type="submit"]')


    def setUp(self):
        """
        Configura el entorno de prueba configurando los datos necesarios,
        creando un usuario e iniciando sesión.
        """
        self.setup_data()
        self.create_user()
        self.login()

    def test_positivo_crear_nuevo_usuario_lider(self):
        self.como_administrador() 
        self.selenium.get(self.live_server_url + "/administrador/crear-usuario")
        
        self.nuevo_usuario_btn.click()
        self.cedula_input.send_keys('1003785324')
        self.nombre_input.send_keys('Juan')
        self.apellido_input.send_keys('Pérez')
        self.email_input.send_keys('juan@example.com')
        self.telefono_input.send_keys('1234567890')
        Select(self.ciudad_select).select_by_index(1)
        self.birthdate_input.send_keys('1990-01-01T00:00')
        Select(self.rol_select).select_by_visible_text("lideres")
        self.crear_usuario_btn.click()

        self.wait_for_element(By.CSS_SELECTOR, 'a[onclick="show()"]')
        self.assertIn('Lista de Usuarios', self.selenium.page_source)
        self.assertIn('Juan Pérez', self.selenium.page_source)

    def test_positivo_crear_nuevo_usuario_gestor(self):
        self.como_administrador() 
        self.selenium.get(self.live_server_url + "/administrador/crear-usuario")
        
        self.nuevo_usuario_btn.click()
        self.cedula_input.send_keys('1004367865')
        self.nombre_input.send_keys('Daniela')
        self.apellido_input.send_keys('Rodriguez')
        self.email_input.send_keys('drodriguez@example.com')
        self.telefono_input.send_keys('55667722')
        Select(self.ciudad_select).select_by_index(3)
        self.birthdate_input.send_keys('1990-01-01T00:00')
        Select(self.rol_select).select_by_visible_text("gestores")
        self.crear_usuario_btn.click()

        self.wait_for_element(By.CSS_SELECTOR, 'a[onclick="show()"]')
        self.assertIn('Lista de Usuarios', self.selenium.page_source)
        self.assertIn('Daniela Rodriguez', self.selenium.page_source)

    def test_negativo_crear_nuevo_usuario_email_invalido(self):
        self.como_administrador()
        self.selenium.get(self.live_server_url + "/administrador/crear-usuario")

        self.nuevo_usuario_btn.click()
        self.cedula_input.send_keys('1002567345')
        self.nombre_input.send_keys('Sara')
        self.apellido_input.send_keys('Gomez')
        self.email_input.send_keys('sara.com')
        self.telefono_input.send_keys('55667722')
        Select(self.ciudad_select).select_by_index(3)
        self.birthdate_input.send_keys('1990-01-01T00:00')
        Select(self.rol_select).select_by_visible_text("gestores")
        self.crear_usuario_btn.click()
        
        self.wait_for_element(By.CSS_SELECTOR, 'a[onclick="show()"]')
        self.assertIn('Lista de Usuarios', self.selenium.page_source)
        self.assertNotIn('Sara Gomez', self.selenium.page_source)

    def test_negativo_crear_nuevo_usuario_cedula_invalida(self):
        self.como_administrador()
        self.selenium.get(self.live_server_url + "/administrador/crear-usuario")

        self.nuevo_usuario_btn.click()
        self.cedula_input.send_keys('jkqswsjkwmjkw')
        self.nombre_input.send_keys('Manuel')
        self.apellido_input.send_keys('Fernandez')
        self.email_input.send_keys('manuf@gmail.com')
        self.telefono_input.send_keys('55667722')
        Select(self.ciudad_select).select_by_index(2)
        self.birthdate_input.send_keys('1990-01-01T00:00')
        Select(self.rol_select).select_by_visible_text("gestores")
        self.crear_usuario_btn.click()

        self.assertEqual(self.cedula_input.get_attribute('value'), '')
        self.wait_for_element(By.CSS_SELECTOR, 'a[onclick="show()"]')
        self.assertIn('Lista de Usuarios', self.selenium.page_source)
        self.assertNotIn('Manuel Fernandez', self.selenium.page_source)






