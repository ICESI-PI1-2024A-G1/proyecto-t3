## Instrucciones principales de ejecución

1. Abrir un terminal cmd o powershell
2. Dirigirse a la carpeta general del proyecto
3. Ejecutar el comando: `.\src\venv\Scripts\activate` para activar el entorno virtual de python configurado.
4. Ejecutar el comando: `python .\src\manage.py makemigrations` para aceptar las entidades/modelos
5. Ejecutar el comando: `python .\src\manage.py migrate` para crear las tablas de los modelos
6. Ejecutar el comando: `python .\src\manage.py runserver` para ejecutar el proyecto.
7. Ir a la url especificada en la consola para acceder a la página.

### Creación de usuarios administradores

1. Ejecutar el comando: `python .\src\manage.py createsuperuser`
2. Introducir un nombre de usuario.
3. Introducir un email.
4. Introducir una contraseña.
5. Confirmar la contraseña.
6. (Si aplica y se requiere) Introducir 'Y' para confirmar que la contraseña es vulnerable.


## Índice de páginas actuales:

**Ejemplo de link:** http://127.0.0.1:8000/{ruta-específica}

### Administradores:

1. [Link principal]/admin -> [127.0.0.1:8000/admin](127.0.0.1:8000/admin)

### Usuarios:

1. [Link principal]/login -> [127.0.0.1:8000/login](http://127.0.0.1:8000/login)
2. [Link principal]/home -> [127.0.0.1:8000/home](http://127.0.0.1:8000/home)
