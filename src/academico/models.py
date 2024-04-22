from django.db import models

from usuarios.models import Director, Docente, Persona


class EstadoSolicitud(models.Model):
    """
    Modelo para representar los estados de una solicitud.

    Atributos:
        estado (AutoField): Identificador único del estado de la solicitud.
        nombre (CharField): Nombre descriptivo del estado.
    """

    estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)


class TipoDeMateria(models.Model):
    """
    Modelo para representar los tipos de materia.

    Atributos:
        tipo (IntegerField): Identificador único del tipo de materia.
        nombre (CharField): Nombre descriptivo del tipo de materia.
    """

    tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32)


class TipoDePrograma(models.Model):
    """
    Modelo para representar los tipos de programa.

    Atributos:
        tipo (IntegerField): Identificador único del tipo de programa.
        nombre (CharField): Nombre descriptivo del tipo de programa.
    """

    tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32)


class Facultad(models.Model):
    """
    Modelo para representar las facultades.

    Atributos:
        id (AutoField): Identificador único de la facultad.
        nombre (CharField): Nombre descriptivo de la facultad.
    """

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)


class Modalidad(models.Model):
    """
    Modelo para representar las modalidades de enseñanza.

    Atributos:
        id (AutoField): Identificador único de la modalidad.
        metodologia (CharField): Descripción de la metodología de enseñanza.
    """

    id = models.AutoField(primary_key=True)
    metodologia = models.CharField(max_length=32)


class Periodo(models.Model):
    """
    Modelo para representar los periodos académicos.

    Atributos:
        semestre (CharField): Identificador único del periodo académico.
        fecha_inicio (DateField): Fecha de inicio del periodo.
        fecha_fin (DateField): Fecha de fin del periodo.
    """

    semestre = models.CharField(primary_key=True, max_length=10)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()


class Espacio(models.Model):
    """
    Modelo para representar los espacios físicos.

    Atributos:
        id (AutoField): Identificador único del espacio.
        tipo (CharField): Tipo de espacio (aula, laboratorio, etc.).
        capacidad (IntegerField): Capacidad máxima del espacio.
    """

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    capacidad = models.IntegerField()


class Programa(models.Model):
    """
    Modelo para representar los programas académicos.

    Atributos:
        codigo (CharField): Código único del programa.
        nombre (CharField): Nombre descriptivo del programa.
        facultad (ForeignKey): Facultad a la que pertenece el programa.
        tipo_de_programa (ForeignKey): Tipo de programa.
        director (ForeignKey): Director del programa.
        estado_solicitud (ForeignKey): Estado actual de la solicitud del programa.
    """

    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=255)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, to_field="id")
    tipo_de_programa = models.ForeignKey(
        TipoDePrograma, on_delete=models.CASCADE, to_field="tipo"
    )
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    estado_solicitud = models.ForeignKey(
        EstadoSolicitud, on_delete=models.CASCADE, to_field="estado"
    )


class Departamento(models.Model):
    """
    Modelo para representar los departamentos académicos.

    Atributos:
        codigo (CharField): Código único del departamento.
        nombre (CharField): Nombre descriptivo del departamento.
    """

    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=255)


class Materia(models.Model):
    """
    Modelo para representar las materias.

    Atributos:
        codigo (IntegerField): Código único de la materia.
        nombre (CharField): Nombre descriptivo de la materia.
        creditos (IntegerField): Número de créditos de la materia.
        departamento (ForeignKey): Departamento al que pertenece la materia.
        tipo_de_materia (ForeignKey): Tipo de materia.
        programas (ManyToManyField): Programas asociados a la materia a través de la malla curricular.
    """

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
    programas = models.ManyToManyField(Programa, through="MallaCurricular")


class MallaCurricular(models.Model):
    """
    Modelo para representar las mallas curriculares.

    Atributos:
        materia (ForeignKey): Materia asociada a la malla.
        programa (ForeignKey): Programa asociado a la malla.
        periodo (ForeignKey): Periodo académico al que pertenece la malla.
    """

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, to_field="codigo")
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, to_field="codigo")
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, to_field="semestre")
    semestre = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["materia", "programa", "periodo"],
                name="unique_materia_programa_periodo",
            )
        ]


class Curso(models.Model):
    """
    Modelo para representar los cursos.

    Atributos:
        nrc (IntegerField): Número de registro del curso.
        grupo (IntegerField): Número de grupo del curso.
        cupo (IntegerField): Cupo máximo del curso.
        materia (ForeignKey): Materia a la que pertenece el curso.
        periodo (ForeignKey): Periodo académico al que pertenece el curso.
    """

    nrc = models.AutoField(primary_key=True)
    grupo = models.IntegerField()
    cupo = models.IntegerField()
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, to_field="codigo")
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, to_field="semestre", default=1)
    intu_generado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('grupo', 'materia','periodo')

class GrupoDeClase(models.Model):
    """
    Modelo para representar los grupos de clase.

    Atributos:
        id (AutoField): Identificador único del grupo de clase.
        nombre (CharField): Nombre descriptivo del grupo de clase.
        clases (ManyToManyField): Clases asociadas al grupo de clase.
    """

    id = models.AutoField(primary_key=True)
    entrega_notas = models.BooleanField(default=False)

class EspacioClase(models.Model):
    """
    Modelo para representar los espacios físicos.

    Atributos:
        id (AutoField): Identificador único del espacio.
        tipo (CharField): Tipo de espacio (aula, laboratorio, etc.).
        capacidad (IntegerField): Capacidad máxima del espacio.
    """

    id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    edificio = models.CharField(max_length=255)
    numero = models.IntegerField()

    class Meta:
        unique_together = ("edificio", "numero")


class Clase(models.Model):
    """
    Modelo para representar las clases.

    Atributos:
        id (AutoField): Identificador único de la clase.
        fecha_inicio (DateTimeField): Fecha y hora de inicio de la clase.
        fecha_fin (DateTimeField): Fecha y hora de fin de la clase.
        espacio_asignado (CharField): Espacio físico asignado para la clase.
        curso (ForeignKey): Curso al que pertenece la clase.
        modalidad (ForeignKey): Modalidad de enseñanza de la clase.
        espacio (ForeignKey): Espacio físico de la clase.
    """

    id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    espacio_asignado = models.ForeignKey(EspacioClase, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, to_field="nrc")
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, to_field="id")
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True, blank=True)
    grupo_clases = models.ForeignKey(GrupoDeClase, on_delete=models.CASCADE, null=True, blank=True)


class Estudiante(Persona):
    """
    Modelo para representar a los estudiantes.

    Atributos:
        codigo (CharField): Código del estudiante.
    """
    codigo = models.CharField(max_length=30, unique=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, to_field="codigo")
    periodo_inscripcion = models.ForeignKey(Periodo, on_delete=models.CASCADE, to_field="semestre")
    cursos = models.ManyToManyField(Curso, through="Inscripcion")

class Inscripcion(models.Model):
    """
    Modelo para representar las inscripciones de los estudiantes.

    Atributos:
        estudiante (CharField): Código del estudiante.
        fecha_inscripcion (DateField): Fecha de inscripción del estudiante.
    """

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, to_field="codigo")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, to_field="nrc")
