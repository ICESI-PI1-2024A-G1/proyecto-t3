import json
import random

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime, timedelta

from .forms import MateriaForm
from .models import (Clase, Curso, Espacio, EstadoSolicitud, Facultad,
                     MallaCurricular, Materia, Periodo, Programa, Modalidad, Docente)
 

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

        return redirect("visualizar clases")
    else:
        espacios = Espacio.objects.all()
        modalidades = Modalidad.objects.all()
        docentes = Docente.objects.all()
        return render(request, "planeacion_materias.html", {'espacios': espacios,'modalidades': modalidades,'docentes': docentes, "curso_id":curso_id})

# Create your views here.


@login_required(login_url="/login")
def crear_curso(request, codigo, periodo):
    if request.method == "POST":
        form = request.POST
        cupo = form["cantidad_de_cupos"]
        # Grupo aleatorio
        grupo = random.randint(1, 9)
        grupo = int(f"00{grupo}")

        try:
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
    else:
        form = MateriaForm()

    materia = get_object_or_404(Materia, codigo=codigo)

    return render(
        request,
        "crear-curso.html",
        {"form": form, "materia": materia, "periodo": periodo},
    )


@login_required(login_url="/login")
def programas(request):
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

    return render(
        request,
        "visualizacion_materias.html",
        {
            "materia": materia,
            "cursos": cursos,
            "periodo_seleccionado": periodo,  # Agregado
            "periodos": Periodo.objects.all(),  # Agregado
        },
    )
    
def args_principal(seleccionado):
    return {
        "Programas posgrado": {"url": "/academico/programas", "seleccionado": seleccionado=="programas"},
        "Materias posgrado": {"url": "/academico/materias", "seleccionado": seleccionado=="materias"},
        "Docentes posgrado": {"url": "/docentes", "seleccionado": seleccionado=="docentes"}
        }
    
def visualizacion_clase(request, nrc, id):
    clase = Clase.objects.get(id=id, curso__nrc=nrc)

    return render(
        request,
        "visualizacion_clases.html",
        {
            "clase": clase,
        },
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
