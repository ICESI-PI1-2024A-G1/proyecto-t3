from django.db import models

from .models import *


class EstadoSolicitud(models.Model):
    estado = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre