from django.db import models


class Ciudad(models.Model):
    id = models.IntegerField(primary_key=True)
    ciudad = models.CharField(max_length=128)


class TipoPersona(models.Model):
    tipo = models.CharField(max_length=32, primary_key=True)


class Persona(models.Model):
    cedula = models.CharField(primary_key=True, max_length=30)
    nombre = models.CharField(max_length=128)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=13)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Director(Persona):
    id = models.IntegerField(unique=True)
    tipo_persona = models.OneToOneField(
        TipoPersona, on_delete=models.CASCADE, related_name="director"
    )


class Docente(Persona):
    numero = models.IntegerField()
    contrato_codigo = models.CharField(max_length=30)
    tipo_persona = models.OneToOneField(
        TipoPersona, on_delete=models.CASCADE, related_name="docente"
    )


