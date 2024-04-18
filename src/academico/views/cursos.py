import random
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from academico.models import Clase, Curso, Docente, GrupoDeClase, Periodo

from .clases import crear_clase


@login_required(login_url="/login")
def crear_curso(request, codigo, periodo):
    """
    Crea un nuevo curso en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        codigo (str): El código de la materia del curso.
        periodo (str): El período académico del curso.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización de materias.

    Raises:
        Http404: Si el período especificado no existe.
    """
    request.user.usuario.init_groups()
    
    if request.method == "POST":
        form = request.POST
        cupo = form["cantidad_de_cupos"]

        grupo_existente = True
        intentos = 0
        max_intentos = 10

        while grupo_existente and intentos < max_intentos:
            grupo = random.randint(1, 9)
            grupo = int(f"00{grupo}")

            if not Curso.objects.filter(grupo=grupo, periodo_id=periodo).exists():
                grupo_existente = False
            else:
                intentos += 1

        if grupo_existente:
            return redirect("visualizacion_materias", codigo=codigo, periodo=periodo)

        try:
            if not Periodo.objects.filter(semestre=periodo).exists():
                raise Http404("El período especificado no existe.")

            Curso.objects.create(
                cupo=cupo,
                grupo=grupo,
                materia_id=codigo,
                periodo_id=periodo,
            )
            return redirect("visualizacion_materias", codigo=codigo, periodo=periodo)
        except IntegrityError as e:
            print("Error al crear el curso. Por favor, inténtelo de nuevo.")
            print(e)

    return redirect("visualizacion_materias", codigo=codigo, periodo=periodo)


@login_required(login_url="/login")
def visualizacion_curso(request, curso_id):
    """
    Vista que muestra la visualización de un curso.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (int): El ID del curso a visualizar.

    Returns:
        HttpResponse: La respuesta HTTP que muestra la visualización del curso.
    """
    request.user.usuario.init_groups()

    curso = get_object_or_404(Curso, nrc=curso_id)
    grupos_clases = []
    total_horas_programadas = timedelta()

    for grupo_clase in GrupoDeClase.objects.filter(clase__curso=curso).distinct().order_by("id"):
        clases = Clase.objects.filter(curso=curso,grupo_clases=grupo_clase).select_related("docente").order_by("fecha_inicio")
        for clase in clases:
            horas_programadas = clase.fecha_fin - clase.fecha_inicio
            clase.horas_programadas = horas_programadas
            total_horas_programadas += horas_programadas
        grupos_clases.append(clases)

    docentes_con_clases = Docente.objects.filter(clase__curso=curso).distinct()
    for docente in docentes_con_clases:
        docente.num_clases = len(Clase.objects.filter(docente=docente, curso=curso))

    return render(
        request,
        "visualizar-curso.html",
        {
            "curso": curso,
            "grupos_clases": grupos_clases,
            "docentes_con_clases": docentes_con_clases,
            "total_horas_programadas": total_horas_programadas,
            "side": "sidebar_curso.html",
        }
        | crear_clase(request, curso_id),
    )
