from django.db import models

from .models import *


class EstadoSolicitud(models.Model):
    estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)

class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=1024)
    fecha_solicitud = models.DateField()

class SolicitudContable(Solicitud):
    presupuesto = models.FloatField()
    cuenta_cobro = models.CharField(max_length=10)
