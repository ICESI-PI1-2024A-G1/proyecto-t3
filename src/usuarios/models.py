from django.contrib.auth.models import User
from django.db import models


class TipoContrato(models.Model):
    """
    Modelo para representar los tipos de contrato.

    Atributos:
        id (AutoField): Identificador único del tipo de contrato.
        tipo (CharField): Descripción del tipo de contrato.
    """

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=128)


class EstadoContrato(models.Model):
    """
    Modelo para representar los estados de un contrato.

    Atributos:
        id (AutoField): Identificador único del estado del contrato.
        estado (CharField): Descripción del estado del contrato.
    """

    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=128)


class Contrato(models.Model):
    """
    Modelo para representar los contratos.

    Atributos:
        codigo (CharField): Código único del contrato.
        fecha_elaboracion (DateField): Fecha de elaboración del contrato.
        tipo_contrato (ForeignKey): Tipo de contrato.
        estado (ForeignKey): Estado del contrato.
    """

    codigo = models.CharField(primary_key=True, max_length=30)
    fecha_elaboracion = models.DateField()
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoContrato, on_delete=models.CASCADE)


class Ciudad(models.Model):
    """
    Modelo para representar las ciudades.

    Atributos:
        id (AutoField): Identificador único de la ciudad.
        ciudad (CharField): Nombre de la ciudad.
    """

    id = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=128, unique=True)


class Persona(models.Model):
    """
    Modelo para representar a las personas.

    Atributos:
        cedula (CharField): Cédula de identidad de la persona (clave primaria).
        nombre (CharField): Nombre de la persona.
        email (EmailField): Dirección de correo electrónico de la persona.
        telefono (CharField): Número de teléfono de la persona.
        ciudad (ForeignKey): Ciudad de residencia de la persona.
    """

    cedula = models.CharField(primary_key=True, max_length=30)
    nombre = models.CharField(max_length=128)
    email = models.EmailField()
    telefono = models.CharField(max_length=13)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    fechaNacimiento = models.DateField()


class Director(Persona):
    """
    Modelo para representar a los directores.

    Atributos:
        oficina (CharField): Oficina del director.
    """

    oficina = models.CharField(max_length=30)

class EstadoDocente(models.Model):
    """
    Modelo para representar los estados de un docente.

    Atributos:
        id (AutoField): Identificador único del estado del docente.
        estado (CharField): Descripción del estado del docente.
    """

    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=128)

class Docente(Persona):
    """
    Modelo para representar a los docentes.

    Atributos:
        contrato_codigo (CharField): Código del contrato del docente.
    """

    contrato_codigo = models.ForeignKey(Contrato, on_delete=models.CASCADE, to_field="codigo")
    estado = models.ForeignKey(EstadoDocente, on_delete=models.CASCADE)
    foto = models.URLField(max_length=200, blank=True, null=True)

class Usuario(models.Model):
    """
    Modelo para representar a los usuarios.
    
    Atributos:
        usuario (OneToOneField): Usuario de Django.
        persona (OneToOneField): Persona asociada al usuario.
    """
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
