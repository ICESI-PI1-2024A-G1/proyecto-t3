from django.db import models

from solicitud.models import EstadoSolicitud
from usuarios.models import Director


class TipoDeMateria(models.Model):
    tipo = models.IntegerField(primary_key=True, auto_created=True, serialize=True)
    nombre = models.CharField(max_length=32)


class TipoDePrograma(models.Model):
    tipo = models.IntegerField(primary_key=True, auto_created=True, serialize=True)
    nombre = models.CharField(max_length=32)


class Facultad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)


class Modalidad(models.Model):
    id = models.AutoField(primary_key=True)
    metodologia = models.CharField(max_length=32)


class Periodo(models.Model):
    semestre = models.CharField(primary_key=True, max_length=10)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()


class Espacio(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    capacidad = models.IntegerField()


class Programa(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=255)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, to_field="id")
    tipo_de_programa = models.ForeignKey(
        TipoDePrograma, on_delete=models.CASCADE, to_field="tipo"
    )
    director = models.ForeignKey(Director, on_delete=models.CASCADE, to_field="cedula")
    estado_solicitud = models.ForeignKey(
        EstadoSolicitud, on_delete=models.CASCADE, to_field="estado"
    )


class Departamento(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=255)


class Materia(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    creditos = models.IntegerField()
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE, to_field="codigo"
    )
    tipo_de_materia = models.ForeignKey(
        TipoDeMateria,
        on_delete=models.CASCADE,
        to_field="tipo",
    )
    programas = models.ManyToManyField(Programa)


class Curso(models.Model):
    nrc = models.IntegerField(primary_key=True)
    grupo = models.IntegerField()
    cupo = models.IntegerField()
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, to_field="codigo")
    periodo = models.ForeignKey(
        Periodo, on_delete=models.CASCADE, to_field="semestre", default=1
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nrc", "periodo"], name="unique_nrc_periodo"
            )
        ]
    # usuario_identificacion = models.CharField(max_length=30)


class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    espacio_asignado = models.CharField(max_length=255, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, to_field="nrc")
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, to_field="id")
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
