from django.db import models

from academico.models import Espacio


class TipoContable(models.Model):
    """
    Modelo para representar los tipos contables.

    Atributos:
        id (AutoField): Identificador único del tipo contable.
        tipo (CharField): Descripción del tipo contable.
    """

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=32)


class EstadoSolicitud(models.Model):
    """
    Modelo para representar los estados de una solicitud.

    Atributos:
        estado (AutoField): Identificador único del estado de la solicitud.
        nombre (CharField): Nombre descriptivo del estado.
    """

    estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)


class Solicitud(models.Model):
    """
    Modelo base para representar una solicitud.

    Atributos:
        id (AutoField): Identificador único de la solicitud.
        descripcion (CharField): Descripción de la solicitud.
        fecha_solicitud (DateField): Fecha de realización de la solicitud.
    """

    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=1024)
    fecha_solicitud = models.DateField()


class SolicitudContable(Solicitud):
    """
    Modelo para representar una solicitud contable.

    Atributos:
        presupuesto (FloatField): Presupuesto asociado a la solicitud contable.
        cuenta_cobro (CharField): Cuenta de cobro asociada a la solicitud contable.
        tipo_contable (ForeignKey): Tipo contable asociado a la solicitud contable.
    """

    presupuesto = models.FloatField()
    cuenta_cobro = models.CharField(max_length=10)
    tipo_contable = models.ForeignKey(TipoContable, on_delete=models.CASCADE)


class SolicitudEspacio(Solicitud):
    """
    Modelo para representar una solicitud de espacio.

    Atributos:
        espacio (ForeignKey): Espacio físico solicitado.
        fecha_inicio (DateField): Fecha de inicio de la solicitud de espacio.
        fecha_fin (DateField): Fecha de fin de la solicitud de espacio.
    """

    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
