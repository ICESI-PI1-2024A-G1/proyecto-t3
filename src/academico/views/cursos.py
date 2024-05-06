import random
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from academico.models import Clase, Curso, Docente, GrupoDeClase, Periodo
from academico.views import verificar_permisos
from solicitud.models import Solicitud, SolicitudViatico

from .clases import obtener_clases


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["lideres"]))
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
@user_passes_test(lambda u: verificar_permisos(u, ["gestores", "directores"]))
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
    clases_Viaticos = []
    total_horas_programadas = timedelta()

    for grupo_clase in GrupoDeClase.objects.filter(clase__curso=curso).distinct().order_by("id"):
        clases = Clase.objects.filter(curso=curso,grupo_clases=grupo_clase).select_related("docente").order_by("fecha_inicio")
        for clase in clases:
            horas_programadas = clase.fecha_fin - clase.fecha_inicio
            clase.horas_programadas = horas_programadas
            total_horas_programadas += horas_programadas
        grupos_clases.append(clases)
    
    for viatico in SolicitudViatico.objects.all():
        if viatico.clase is not None:
            clases_Viaticos.append(viatico.clase.id)

    docentes_con_clases = Docente.objects.filter(clase__curso=curso).distinct()
    for docente in docentes_con_clases:
        docente.num_clases = len(Clase.objects.filter(docente=docente, curso=curso))
            
    return render(
        request,
        "visualizar-curso.html",
        {
            "curso": curso,
            "viaticos": clases_Viaticos, 
            "grupos_clases": grupos_clases,
            "docentes_con_clases": docentes_con_clases,
            "total_horas_programadas": total_horas_programadas,
            "side": "sidebar_curso.html",
        }
        | obtener_clases(request, curso_id)
    )

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["gestores"]))
def change_notas(request, curso_id, grupoId):
    """
    Edita el valor del atributo entrega_notas de un grupo de clases en un curso.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (int): Recibe el id del curso.
        grupoId (int): Recibe el id del grupo de clases.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del curso.
    Raises:
        Http404: Si el curso o el grupo no existen.
    """
    request.user.usuario.init_groups()
    grupo = get_object_or_404(GrupoDeClase, id=grupoId)
    curso = get_object_or_404(Curso, nrc=curso_id)
    if request.method == "POST":
        grupo.entrega_notas=not grupo.entrega_notas
        grupo.save()
    return redirect("visualizar-curso", curso_id=curso.nrc)


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["gestores"]))
def change_intu(request, curso_id):
    """
    Edita el valor del atributo intu_generado de un grupo de clases en un curso.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (int): Recibe el id del curso.
        grupoId (int): Recibe el id del grupo de clases.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del curso.
    Raises:
        Http404: Si el curso o el grupo no existen.
    """
    request.user.usuario.init_groups()
    curso = get_object_or_404(Curso, nrc=curso_id)
    if request.method == "POST":
        curso.intu_generado = not curso.intu_generado
        curso.save()
    return redirect("visualizar-curso", curso_id=curso.nrc)

        