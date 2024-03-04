from django.db import models


class TipoContrato(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=128)


class EstadoContrato(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=128)


class Contrato(models.Model):
    codigo = models.CharField(primary_key=True, max_length=30)
    fecha_elaboracion = models.DateField()
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoContrato, on_delete=models.CASCADE)


class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=128)


class Persona(models.Model):
    cedula = models.CharField(primary_key=True, max_length=30)
    nombre = models.CharField(max_length=128)
    email = models.EmailField()
    telefono = models.CharField(max_length=13)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)


class Director(Persona):
    oficina = models.CharField(max_length=30)


class Docente(Persona):
    contrato_codigo = models.CharField(max_length=30)
