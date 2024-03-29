import json
import random
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import MateriaForm
from .models import (Clase, Curso, Docente, Espacio, EstadoSolicitud, Facultad,
                     MallaCurricular, Materia, Modalidad, Periodo, Programa)


@login_required(login_url="/login")
def crear_clase(request, curso_id):
    if request.method == "POST":
        start_day = datetime.strptime(request.POST.get("start_day"), "%Y-%m-%dT%H:%M")
        end_day = datetime.strptime(request.POST.get("end_day"), "%Y-%m-%dT%H:%M")
        tipo_espacio = int(request.POST.get("tipo_espacio"))
        modalidad_clase = int(request.POST.get("modalidad_clase"))
        num_semanas = int (request.POST.get("num_semanas"))
        docente_cedula = (request.POST.get("docente_clase"))

        if not Docente.objects.filter(cedula=docente_cedula).exists():
            return render(request, "error.html", {"mensaje": "El docente no existe."})

        if not Curso.objects.filter(nrc=curso_id).exists():
            return render(request, "error.html", {"mensaje": "El curso no existe."})

        if not Espacio.objects.filter(id=tipo_espacio).exists():
            return render(request, "error.html", {"mensaje": "El espacio no existe."})

        if not Modalidad.objects.filter(id=modalidad_clase).exists():
            return render(request, "error.html", {"mensaje": "La modalidad no existe."})

        docente = Docente.objects.get(cedula=docente_cedula)

        for _ in range(num_semanas):
            clase = Clase.objects.create(
                fecha_inicio=start_day,
                fecha_fin=end_day,
                espacio_asignado=None,
                curso_id=curso_id,
                espacio_id=tipo_espacio,
                modalidad_id=modalidad_clase,
                docente = docente

            )
            start_day += timedelta(days=7)
            end_day += timedelta(days=7)   

        return redirect("visualizar-curso", curso_id=curso_id)
    else:
        espacios = Espacio.objects.all()
        modalidades = Modalidad.objects.all()
        docentes = Docente.objects.all()
        return {
            "espacios": espacios,
            "modalidades": modalidades,
            "docentes": docentes,
            "curso_id": curso_id,
        }


@login_required(login_url="/login")
def editar_clase(request, clase_id):
    clase = get_object_or_404(Clase,id=clase_id)
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        espacio_asignado = request.POST.get("espacio_asignado")
        tipo_espacio_id = request.POST.get("tipo_espacio")
        modalidad_id = request.POST.get("modalidad_clase")
        docente_cedula = request.POST.get("docente_clase")

        if not all([fecha_inicio, fecha_fin, tipo_espacio_id, modalidad_id, docente_cedula]):
            return render(request, "error.html", {"mensaje": "Todos los campos son requeridos."})

        try:
            tipo_espacio = Espacio.objects.get(id=tipo_espacio_id)
            modalidad = Modalidad.objects.get(id=modalidad_id)
            docente = Docente.objects.get(cedula=docente_cedula)
        except (Espacio.DoesNotExist, Modalidad.DoesNotExist, Docente.DoesNotExist):
            return render(request, "error.html", {"mensaje": "Uno o más de los IDs proporcionados no existen."})

        clase.fecha_inicio = fecha_inicio
        clase.fecha_fin = fecha_fin
        clase.espacio_asignado = espacio_asignado
        clase.espacio = tipo_espacio
        clase.modalidad = modalidad
        clase.docente = docente
        clase.save()
        
    return redirect("visualizar-curso", curso_id=clase.curso.nrc)
# Create your views here.


@login_required(login_url="/login")
def crear_curso(request, codigo, periodo):
    """
    Creates a new course with the specified code and period.

    Args:
        request (HttpRequest): The HTTP request object.
        codigo (str): The code of the course.
        periodo (str): The period of the course.

    Returns:
        HttpResponseRedirect: Redirects to the "visualizacion_materias" view.

    Raises:
        Http404: If the specified period does not exist.
    """
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
def programas(request):
    """
    View function for displaying a list of programs.

    This view function handles the logic for displaying a list of programs based on various filters and search queries.
    It also handles pagination of the program list.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template with the program list.

    """
    programas = Programa.objects.all()

    # Búsqueda y filtrado
    if request.method == "GET":
        periodo_seleccionado = request.GET.get("periodo", None)
        query = request.GET.get("q", None)
        facultad = request.GET.get("facultad", None)
        estado = request.GET.get("estado", None)
        ordenar_por = request.GET.get("ordenar_por", None)

        if periodo_seleccionado:
            programas = programas.filter(periodo__semestre=periodo_seleccionado)

        if query:
            programas = programas.filter(
                Q(nombre__icontains=query)
                | Q(facultad__nombre__icontains=query)
                | Q(director__nombre__icontains=query)
                | Q(nombre__icontains=query)
            )

        if facultad:
            programas = programas.filter(facultad__id=facultad)
        if estado:
            programas = programas.filter(estado_solicitud__estado=estado)

        if ordenar_por:
            programas = programas.order_by(ordenar_por)

    paginator = Paginator(programas, 10)

    # Paginación
    page_number = request.GET.get("page")
    try:
        programas = paginator.page(page_number)
    except PageNotAnInteger:
        programas = paginator.page(1)
    except EmptyPage:
        programas = paginator.page(paginator.num_pages)

    periodos_academicos = Periodo.objects.all()
    facultades = Facultad.objects.all()
    estados = EstadoSolicitud.objects.all()

    return render(
        request,
        "programas.html",
        {
            "programas": programas,
            "periodos_academicos": periodos_academicos,
            "facultades": facultades,
            "estados": estados,
            "side": "sidebar_principal.html",
            "side_args": args_principal("programas"),
        },
    )

def materias(request):
    """
    View function for displaying a list of materias.

    This function retrieves all the materias and programas from the database.
    It also handles search, filtering, and pagination of the materias.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the list of materias.

    """
    materias = Materia.objects.all()
    programas = Programa.objects.all()

    # Búsqueda y filtrado
    if request.method == "GET":
        query = request.GET.get("q", None)
        ordenar_por = request.GET.get("ordenar_por", None)
        programa = request.GET.get("programa", None)

        if query:
            materias = materias.filter(
                Q(nombre__icontains=query) | Q(departamento__nombre__icontains=query)
            )

        if programa:
            materias = materias.filter(programas__codigo=programa)

        if ordenar_por:
            materias = materias.order_by(ordenar_por)

    paginator = Paginator(materias, 10)

    # Paginación
    page_number = request.GET.get("page")
    try:
        materias = paginator.page(page_number)
    except PageNotAnInteger:
        materias = paginator.page(1)
    except EmptyPage:
        materias = paginator.page(paginator.num_pages)

    return render(
        request,
        "materias.html",
        {
            "materias": materias,
            "programas": programas,
            "side": "sidebar_principal.html",
            "side_args": args_principal("materias"),
        },
    )

@login_required(login_url="/login")
def programa(request, codigo, periodo):
    programa = get_object_or_404(Programa,codigo=codigo)
    materias = MallaCurricular.objects.filter(
        programa__codigo=codigo, periodo__semestre=periodo
    )

    malla_curricular = {}
    tamaño = 0
    creditos_totales = 0
    cursos_totales = 0

    for materia in materias:
        materia.materia.color = color_suave()
        creditos_totales += materia.materia.creditos
        cursos_totales += 1
        if materia.semestre not in malla_curricular.keys():
            tamaño = 1
            malla_curricular[materia.semestre] = []
        malla_curricular[materia.semestre].append(materia.materia)

    semestres = len(malla_curricular.keys())

    return render(
        request,
        "programa.html",
        {
            "programa": programa,
            "periodos": Periodo.objects.all(),
            "periodo_seleccionado": periodo,
            "malla": malla_curricular,
            "tamaño": tamaño,
            "creditos_totales": creditos_totales,
            "cursos_totales": cursos_totales,
            "semestres": semestres,
            "side": "sidebar_programa.html",
            "modalidad": obtener_modalidad(materias),
        },
    )

def actualizar_malla(request, codigo, periodo):
    body = json.loads(request.body.decode('utf-8'))
    for key in body:
        if len(MallaCurricular.objects.filter(programa__codigo=codigo, periodo__semestre=periodo))<1:
            continue
        if MallaCurricular.objects.filter(materia__codigo=key,programa__codigo=codigo,periodo__semestre=periodo).exists():
            malla = MallaCurricular.objects.get(materia__codigo=key, programa__codigo=codigo, periodo__semestre=periodo)
            malla.semestre=body[key]
            malla.save()
    return redirect("programa",codigo=codigo,periodo=periodo)


@login_required(login_url="/login")
def malla_curricular(request, codigo, periodo):
    programa= get_object_or_404(Programa,codigo=codigo)
    malla = MallaCurricular.objects.filter(
        programa__codigo=codigo, periodo__semestre=periodo
    )

    semestres = set()
    for materia in malla:
        semestres.add(materia.semestre)

    paginator = Paginator(malla, 10)

    # Paginación
    page_number = request.GET.get("page")
    try:
        malla = paginator.page(page_number)
    except PageNotAnInteger:
        malla = paginator.page(1)
    except EmptyPage:
        malla = paginator.page(paginator.num_pages)

    return render(
        request,
        "malla_programa.html",
        {
            "programa": programa,
            "semestres": semestres,
            "malla": malla,
            "num_materias": len(malla),
            "periodos": Periodo.objects.all(),
            "periodo_seleccionado": periodo,
            "side": "sidebar_programa.html",
        },
    )


def color_suave():
    # Seleccionar un color de la lista de forma aleatoria
    color = random.choice([1, 2, 3])
    return color

def visualizacion_materia(request, codigo, periodo):
    materia = Materia.objects.get(codigo=codigo)
    cursos = Curso.objects.filter(materia__codigo=codigo, periodo__semestre=periodo)

    periodos = Periodo.objects.all()
    cursos.color = color_suave()

    return render(
        request,
        "visualizacion_materias.html",
        {
            "materia": materia,
            "cursos": cursos,
            "periodo_seleccionado": periodo,  # Agregado
            "periodos": Periodo.objects.all(),  # Agregado
            "side": "sidebar_materias.html",
        },
    )

def args_principal(seleccionado):
    return {
        "Programas posgrado": {"url": "/academico/programas", "seleccionado": seleccionado=="programas"},
        "Materias posgrado": {"url": "/academico/materias", "seleccionado": seleccionado=="materias"},
        "Docentes posgrado": {"url": "/docentes", "seleccionado": seleccionado=="docentes"}
        }

def visualizacion_clase(request, nrc, id):
    """
    Render the visualizacion_clases.html template with the specified class.

    Args:
        request (HttpRequest): The HTTP request object.
        nrc (str): The NRC (Número de Registro de Curso) of the class.
        id (int): The ID of the class.

    Returns:
        HttpResponse: The rendered HTML response.

    Raises:
        Clase.DoesNotExist: If the class with the specified NRC and ID does not exist.
    """
    clase = Clase.objects.get(id=id, curso__nrc=nrc)

    return render(
        request,
        "visualizacion_clases.html",
        {
            "clase": clase,
        },
    )

@login_required(login_url="/login")
def visualizacion_curso(request, curso_id):
    """
    View function for displaying course information.

    Args:
        request (HttpRequest): The HTTP request object.
        curso_id (int): The ID of the course to be displayed.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    curso = get_object_or_404(Curso, nrc=curso_id)
    clases = Clase.objects.filter(curso=curso).select_related('docente')
    docentes_con_clases = Docente.objects.filter(clase__curso=curso).distinct()

    total_horas_programadas = timedelta()
    for clase in clases:
        horas_programadas = clase.fecha_fin - clase.fecha_inicio
        clase.horas_programadas = horas_programadas
        total_horas_programadas += horas_programadas

    return render(
        request,
        "visualizar-curso.html",
        {
            "curso": curso,
            "clases": clases,
            "docentes_con_clases": docentes_con_clases,
            "total_horas_programadas": total_horas_programadas,
            "side": "sidebar_curso.html",
        } | crear_clase(request, curso_id),
    )


def obtener_modalidad(malla):
    modalidades = ["NO ESPECIFICADO"]

    for materia in malla:
        try:
            for curso in Curso.objects.get(materia__codigo=materia.codigo):
                for clase in Clase.objects.get(curso_id=curso.id):
                    modalidades.append(clase.modalidad)
        except:
            continue

    return max(set(modalidades), key=modalidades.count)
