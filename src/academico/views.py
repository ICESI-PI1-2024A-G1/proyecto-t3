import random

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import MateriaForm
from .models import (Clase, EstadoSolicitud, Facultad, MallaCurricular,
                     Materia, Periodo, Programa, Curso)


def crear_clase(request):
    if request.method == "POST":
        start_day = request.POST("start_day")
        end_day = request.POST("end_day")
        time_I = request.POST.get("time_I")
        time_F = request.POST.get("time_F")
        weeks = request.POST.get("weeks")
        mode = request.POST.get("mode")
        curso_id = request.POST.get("curso_id")

        new_class = Clase(
            start_day=start_day,
            end_day=end_day,
            time_I=time_I,
            time_F=time_F,
            weeks=weeks,
            mode=mode,
            curso_id=curso_id,
        )
        new_class.save()

        return redirect("visualizar clases")
    else:
        return render(request, "planeacion_materias.html")


# Create your views here.


def crear_curso(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            mensaje = "Curso creado exitosamente"
            return render(request, "crear-curso.html", {"form": form, "mensaje": mensaje})
    else:
        form = MateriaForm()

    materias = Materia.objects.all()
    periodos = Periodo.objects.all()

    return render(
        request,
        "crear-curso.html",
        {"form": form, "materias": materias, "periodos": periodos},
    )


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
    page_number = request.GET.get('page')
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
        },
    )


def programa(request, codigo, periodo):
    programa = Programa.objects.get(codigo=codigo)
    materias = MallaCurricular.objects.filter(
        programa__codigo=codigo, periodo__semestre=periodo
    )
    malla_curricular = {}
    
    for materia in materias:
        if materia.semestre not in malla_curricular.keys():
            malla_curricular[materia.semestre] = []
        malla_curricular[materia.semestre].append(materia.materia)
            
    return render(
        request,
        "programa.html",
        {
            "programa": programa,
            "periodos": Periodo.objects.all(),
            "periodo_selecionado": periodo,
            "malla": malla_curricular,
        },
    )


# Lista de colores
colores = [
    "azul",
    "rojo",
    "verde",
    "amarillo",
    "naranja",
    "rosa",
    "violeta",
    "turquesa",
]


def color_suave():
    # Seleccionar un color de la lista de forma aleatoria
    color = random.choice(colores)
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
