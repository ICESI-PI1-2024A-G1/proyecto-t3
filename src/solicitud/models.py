from django.db import models

from academico.models import Clase
from usuarios.models import Docente, Usuario


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
    fecha_solicitud = models.DateField(auto_now_add=True)

class SolicitudEspacio(Solicitud):
    """
    Modelo para representar una solicitud de espacio.
    
    Atributos:
        estado (ForeignKey): Estado de la solicitud.
        responsable (ForeignKey): Usuario responsable de la solicitud.
        clases (ManyToManyField): Clases asociadas a la solicitud.
    """

    estado = models.ForeignKey(EstadoSolicitud, on_delete=models.CASCADE, null=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    clases = models.ManyToManyField(Clase, through='SolicitudClases')

class SolicitudClases(models.Model):
    solicitud = models.ForeignKey(SolicitudEspacio, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)


class PropositoViaje(models.Model):
    id = models.AutoField(primary_key=True)
    proposito = models.CharField(max_length=128)

class SolicitudViatico(Solicitud):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    fecha_ida = models.DateField()
    fecha_vuelta = models.DateTimeField()
    propositoViaje = models.ForeignKey(PropositoViaje, on_delete=models.CASCADE, to_field="id")
    tiquete= models.BooleanField()
    hospedaje= models.BooleanField()
    alimentacion= models.BooleanField()
