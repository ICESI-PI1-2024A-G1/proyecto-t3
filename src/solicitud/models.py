from django.db import models

from academico.models import Espacio


class TipoContable(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=32)


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
    tipo_contable = models.ForeignKey(TipoContable, on_delete=models.CASCADE)


class SolicitudEspacio(Solicitud):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
