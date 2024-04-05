import json
import os
import random
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib import utils
from collections import Counter
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.platypus import Paragraph
from openpyxl import Workbook
import pandas as pd

from ccsa_project import settings
from .models import Programa
from django.templatetags.static import static

from .forms import MateriaForm
from .models import (Clase, Curso, Docente, Espacio, EstadoSolicitud, Facultad,
                     MallaCurricular, Materia, Modalidad, Periodo, Programa)


@login_required(login_url="/login")
def crear_clase(request, curso_id):
    """
    Crea una nueva clase para un curso en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        curso_id (str): Recibe el codigo del curso.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualizacion clases dentro del curso.

    Raises:
        Http404: Si el curso no existe.
    
    """
    if request.method == "POST":
        
        start_day = datetime.strptime(request.POST.get("start_day"), "%Y-%m-%dT%H:%M")
        end_day = datetime.strptime(request.POST.get("end_day"), "%Y-%m-%dT%H:%M")

        tipo_espacio = int(request.POST.get("tipo_espacio"))
        modalidad_clase = int(request.POST.get("modalidad_clase"))
        num_semanas_str = (request.POST.get("num_semanas", "1"))
        num_semanas = 1 if  num_semanas_str == "" else int(num_semanas_str)
        docente_cedula = request.POST.get("docente_clase")

        if not Curso.objects.filter(nrc=curso_id).exists():
            raise Http404("El curso no existe.")

        if not Espacio.objects.filter(id=tipo_espacio).exists():
            raise Http404("El espacio no existe.")

        if not Modalidad.objects.filter(id=modalidad_clase).exists():
            raise Http404("La modalidad no existe.")
        
        if docente_cedula is not None and docente_cedula != "None":            
            docente = Docente.objects.get(cedula=docente_cedula)
        else:
            docente = None  

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

    """
    Permite editar los atributos de una clase

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): El código de la clase a editar.
        

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualizacion clases dentro del curso.

    Raises:
        Http404: Si la clase no existe.

    """
    clase = get_object_or_404(Clase,id=clase_id)
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        tipo_espacio_id = request.POST.get("tipo_espacio_e")
        modalidad_id = request.POST.get("modalidad_clase_e")
        docente_cedula = request.POST.get("docente_clase_e")

        if (fecha_inicio==None or fecha_fin==None or tipo_espacio_id==None or modalidad_id==None):
             raise Http404("Todos los campos son requeridos.")

        try:
            tipo_espacio = Espacio.objects.get(id=tipo_espacio_id)       
        except (Espacio.DoesNotExist):
            raise Http404("Tipo de espacio no existe.")

        try:
            modalidad = Modalidad.objects.get(id=modalidad_id)    
        except (Modalidad.DoesNotExist):
            raise Http404("Modalidad no existe.")
        
        if docente_cedula is not None and docente_cedula != "None":
            try:
                docente = Docente.objects.get(cedula=docente_cedula)
                
            except (Docente.DoesNotExist):
                raise Http404("Docente no existe.")
        else:
            docente = None
            
        
        clase.fecha_inicio = fecha_inicio
        clase.fecha_fin = fecha_fin
        clase.espacio = tipo_espacio
        clase.modalidad = modalidad
        clase.docente = docente
        clase.save()
        
    return redirect("visualizar-curso", curso_id=clase.curso.nrc)
# Create your views here.


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
    Vista para mostrar la lista de programas académicos.

    Esta vista permite realizar búsquedas y filtrados en la lista de programas académicos.
    Los programas se pueden filtrar por periodo, facultad, estado y se pueden ordenar por diferentes criterios.
    Además, se implementa la paginación para mostrar los programas de forma organizada.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP que contiene la página de programas académicos.

    Raises:
        None
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
    Vista que muestra la lista de materias.

    Esta vista recibe una solicitud HTTP y devuelve una respuesta HTTP que muestra una lista de materias.
    La lista de materias se puede filtrar y ordenar según los parámetros proporcionados en la solicitud GET.

    Parámetros:
    - request: La solicitud HTTP recibida.

    Retorna:
    - Una respuesta HTTP que muestra una lista de materias.

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
    """
    Renderiza la plantilla 'programa.html' con información del programa y datos del currículo.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        codigo (str): El código del programa.
        periodo (str): El período del semestre.

    Returns:
        HttpResponse: La plantilla 'programa.html' renderizada con las siguientes variables de contexto:
            - 'programa': El objeto Programa.
            - 'periodos': Todos los objetos Periodo.
            - 'periodo_seleccionado': El período seleccionado.
            - 'malla': Un diccionario que representa el currículo, donde las claves son los semestres y los valores son listas de Materias.
            - 'tamaño': El tamaño del currículo.
            - 'creditos_totales': El número total de créditos en el currículo.
            - 'cursos_totales': El número total de cursos en el currículo.
            - 'semestres': El número de semestres en el currículo.
            - 'side': La plantilla de la barra lateral a incluir.
            - 'modalidad': La modalidad del currículo.

    """
    programa = get_object_or_404(Programa,codigo=codigo)
    materias = MallaCurricular.objects.filter(
        programa__codigo=codigo, periodo__semestre=periodo
    )

    malla_curricular = {}
    tamaño = 0
    creditos_totales = 0
    cursos_totales = 0
    docentes_con_clase = []

    for materia in materias:
        materia.materia.color = color_suave()
        creditos_totales += materia.materia.creditos
        cursos_totales += 1
        docentes_con_clase+=Docente.objects.filter(clase__curso__materia=materia.materia, clase__curso__periodo__semestre=periodo).distinct()
        if materia.semestre not in malla_curricular.keys():
            tamaño = 1
            malla_curricular[materia.semestre] = []
        malla_curricular[materia.semestre].append(materia.materia)

    semestres = len(malla_curricular.keys())
    
    docentes = set()
    for docente in docentes_con_clase:
        docente.lista_materias = Materia.objects.filter(curso__clase__docente=docente).distinct()
        docentes.add(docente)
    

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
            "docentes_con_clases": docentes,
            "total_docentes": len(docentes),
            "side": "sidebar_programa.html",
            "modalidad": obtener_modalidad(materias),
        },
    )

def actualizar_malla(request, codigo, periodo):
    """
    Actualiza la malla curricular de un programa académico para un periodo específico.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        codigo (str): El código del programa académico.
        periodo (str): El periodo para el cual se actualizará la malla curricular.

    Returns:
        HttpResponseRedirect: Una redirección a la vista del programa académico actualizado.
    """
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
    """
    Función de vista para mostrar la malla curricular de un programa.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        codigo (str): El código del programa.
        periodo (str): El semestre de la malla curricular.

    Returns:
        HttpResponse: El objeto de respuesta HTTP que contiene la plantilla renderizada.
    """
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
    """
    Retorna un color suave seleccionado aleatoriamente de una lista.
    La lista de colores está definida en el CSS.

    Returns:
        int: Un número entero que representa el color seleccionado.
    """
    color = random.choice([1, 2, 3])
    return color

@login_required(login_url="/login")
def visualizacion_materia(request, codigo, periodo):
    """
    Renderiza la página de visualización de información de una materia.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        codigo (str): El código de la materia a visualizar.
        periodo (str): El periodo académico en el que se desea visualizar la materia.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la página de visualización de la materia.

    Raises:
        Http404: Si no se encuentra la materia con el código especificado.
    """
    
    materia = get_object_or_404(Materia, codigo=codigo)
    cursos = Curso.objects.filter(materia__codigo=codigo, periodo__semestre=periodo)
    cursos_totales = Curso.objects.filter(materia__codigo=codigo)
    c_num = Curso.objects.filter(periodo=periodo, materia=codigo).count()
    c_numT = Curso.objects.filter(materia=codigo).count()
    clases = Clase.objects.all()

    docentes_con_clase = []
    for curso in cursos:
        docentes = Docente.objects.filter(clase__curso=curso).distinct()
        for docente in docentes:
            if docente not in docentes_con_clase:
                docente.cursos = []
                docentes_con_clase.append(docente)
            docentes_con_clase[docentes_con_clase.index(docente)].cursos.append(curso)
    
    total_docentes_asignados = 0
    total_clases = 0
    
    for curso in cursos_totales:
        for clase in clases:  
            if clase.curso == curso.nrc:
                total_docentes_asignados += 1
                total_clases += 1
            else:
                total_clases += 1
    
    cursos.color = color_suave()

    return render(
        request,
        "visualizacion_materias.html",
        {
            "materia": materia,
            "cursos": cursos,
            "periodo_seleccionado": periodo,
            "periodos": Periodo.objects.all(),
            "side": "sidebar_materias.html",
            "c_num": c_num,
            "c_numT": c_numT,
            "total_asignados": total_docentes_asignados,
            "docentes_con_clases": docentes_con_clase,
            "total_docentes": len(docentes_con_clase),
            "total_clases": total_clases,
        },
    )

def args_principal(seleccionado):
    """
    Genera un diccionario con la información de los menús de la barra lateral del menú principal.

    Args:
        seleccionado (str): El menú seleccionado actualmente.

    Returns:
        dict: Un diccionario con la información de los menús, donde la clave es el nombre del menú y el valor es otro diccionario con la URL y si está seleccionado o no.
    """
    return {
        "Programas posgrado": {"url": "/academico/programas", "seleccionado": seleccionado=="programas"},
        "Materias posgrado": {"url": "/academico/materias", "seleccionado": seleccionado=="materias"},
        "Docentes posgrado": {"url": "/docentes", "seleccionado": seleccionado=="docentes"}
    }

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
    curso = get_object_or_404(Curso, nrc=curso_id)
    clases = Clase.objects.filter(curso=curso).select_related('docente')
    docentes_con_clases = Docente.objects.filter(clase__curso=curso).distinct()
    for docente in docentes_con_clases:
        docente.num_clases = len(Clase.objects.filter(docente=docente, curso=curso))

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
    """
    Obtiene la modalidad de un programa con base en sus clases.

    Parámetros:
    - malla (list): Lista de materias de la malla curricular del programa.

    Retorna:
    - str: La modalidad más frecuente encontrada en las clases del programa.
    """
    modalidades = ["NO ESPECIFICADO"]

    for materia in malla:
        try:
            for clase in Clase.objects.filter(curso__materia=materia.materia):
                modalidades.append(clase.modalidad.metodologia)
        except:
            continue
    return max(set(modalidades), key=modalidades.count)

def export_to_pdf(request, codigo_programa, periodo):
    programa = Programa.objects.select_related('facultad', 'director').get(codigo=codigo_programa)
    malla_curricular = MallaCurricular.objects.filter(programa__codigo=codigo_programa, periodo__semestre=periodo)
    materias = [materia.materia for materia in malla_curricular]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="programa.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    # Logo 
    logo_width = 1.5 * inch
    logo_height = 0.75 * inch

    '''
    Ejecutar collectatic al final de la implementación
    logo_path = os.path.join(settings.STATIC_ROOT, 'img/logo-app.jpg')
    p.drawInlineImage(logo_path, 50, 750 - logo_height, width=logo_width, height=logo_height)
    '''

    # Texto encabezado
    p.setFont("Helvetica", 12)
    p.drawString(150 + logo_width, 750 - logo_height - 15, "Universidad Icesi")
    p.drawString(130 + logo_width, 730, "Programación académica")

    p.setFont("Helvetica", 12)

    # Posición inicial 
    y = 640

    y_threshold = 50

    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, y, "Información general del programa")
    y -= 20  

    # Información general del programa
    informacion_general = [
        ("Nombre del programa: ", programa.nombre),
        ("Periodo: ", periodo),
        ("Facultad: ", programa.facultad.nombre),
        ("Director de programa: ", programa.director.nombre),
        ("Email del director: ", programa.director.email),
        ("Teléfono del director: ", programa.director.telefono),
        ("Modalidad: ", obtener_modalidad(materias))
    ]

    for label, value in informacion_general:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(70, y, label)
        p.setFont("Helvetica", 12)
        p.drawString(70 + p.stringWidth(label, "Helvetica-Bold", 12), y, value)
        y -= 15

    y -= 20  

    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, y, "Malla Curricular")
    y -= 20  

    # Contenido de la tabla de cursos y docentes
    for malla_curricular in malla_curricular:
        if y < y_threshold:
            p.showPage()
            y = 750

        materia = malla_curricular.materia
        
        p.setFont("Helvetica-Bold", 12)
        p.drawString(70, y, f"Materia: {materia.nombre}")
        y -= 10
        
        cursos = Curso.objects.filter(materia=materia, periodo__semestre=periodo)
        if cursos.exists(): 
            for curso in cursos:
                clases = Clase.objects.filter(curso=curso)
                docentes = [clase.docente for clase in clases] if clases.exists() else ""
                
                # Datos para la tabla
                data = [["NRC Curso", "Clase", "Docente"]]
                for clase in clases:
                    docente_nombre = clase.docente.nombre if clase.docente else 'No asignado'
                    fecha_inicio = clase.fecha_inicio.strftime('%Y-%m-%d de %I %p')
                    fecha_fin = clase.fecha_fin.strftime('%I %p')
                    data.append([curso.nrc, f"{fecha_inicio} a {fecha_fin}", docente_nombre])

                # Estilo de la tabla
                style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

                # Crear tabla y aplicar estilo
                tabla = Table(data)
                tabla.setStyle(style)

                # Dibujar tabla
                tabla.wrapOn(p, 0, 0)
                
                tabla_height = tabla._height

                if y - tabla_height < y_threshold:
                    p.showPage()
                    y = 750

                tabla.drawOn(p, 70, y - tabla_height)

                y -= tabla_height + 20

            y -=40
        else: 
            p.drawString(70, y-5, "No hay cursos registrados para esta materia")
            y -= 40

    # Sección de "Estadísticas"
    if y < y_threshold:
        p.showPage()
        y = 750

    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, y, "Estadísticas")
    y -= 60  

    # Gráfico circular de tipos de espacios de las clases, cursos del programa y periodo seleccionado
    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, y - 130, "Tipos de espacios de las clases")  # Título para el gráfico circular
    clases = Clase.objects.filter(curso__materia__programas__codigo=codigo_programa, curso__periodo__semestre=periodo)
    tipos_espacios = [clase.espacio.tipo for clase in clases]
    tipos_espacios_counter = Counter(tipos_espacios)
    tipos_espacios_data = list(tipos_espacios_counter.values())
    tipos_espacios_labels = list(tipos_espacios_counter.keys())

    drawing = Drawing(200, 150)
    pie = Pie()
    pie.x = 60
    pie.y = 60
    pie.width = 120
    pie.height = 120
    pie.data = tipos_espacios_data
    pie.labels = tipos_espacios_labels
    pie.sideLabels = True
    pie.slices.strokeWidth = 0.5
    pie.slices.strokeColor = colors.white
    light_colors = [colors.lightcoral, colors.lightgreen, colors.lightblue, colors.lightgoldenrodyellow, colors.lightcyan, colors.lightpink, colors.lightsalmon, colors.lightseagreen, colors.lightskyblue, colors.lightsteelblue, colors.lightyellow, colors.lightgrey]
    for i in range(len(tipos_espacios_labels)):
        pie.slices[i].fillColor = light_colors[i % len(light_colors)]

    drawing.add(pie)
    renderPDF.draw(drawing, p, 70, y - 150)

    # Gráfico de barras de la cantidad de clases por docente en el programa del periodo seleccionado
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y - 130, "Cantidad de clases por docente")  
    docentes = Docente.objects.filter(clase__curso__materia__programas__codigo=codigo_programa, clase__curso__periodo__semestre=periodo).distinct()
    docentes_clases = {}
    for docente in docentes:
        docentes_clases[docente.nombre] = docente.clase_set.count()
    no_asignado = Clase.objects.filter(curso__materia__programas__codigo=codigo_programa, curso__periodo__semestre=periodo, docente__isnull=True).count()
    if no_asignado > 0:
        docentes_clases['No asignado'] = no_asignado
    docentes_nombres = list(docentes_clases.keys())
    docentes_clases = list(docentes_clases.values())
    drawing = Drawing(200, 150)
    bar = VerticalBarChart()
    bar.x = 60
    bar.y = 60
    bar.width = 120
    bar.height = 120
    bar.data = [docentes_clases]
    bar.categoryAxis.categoryNames = docentes_nombres
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = max(docentes_clases) + 1

    for i in range(len(docentes_nombres)):
        bar.bars[i].fillColor = random.choice(light_colors)

    drawing.add(bar)
    renderPDF.draw(drawing, p, 350, y - 150)

    # Gráfico circular de cantidad de clases por materia (con porcentajes dentro de los slices)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, y - 300, "Cantidad de clases por materia")

    # Obtener todas las clases y contarlas por materia
    clases = Clase.objects.filter(curso__materia__programas__codigo=codigo_programa, curso__periodo__semestre=periodo)
    materias_counter = Counter([clase.curso.materia.nombre for clase in clases])
    total_clases = len(clases)  # Calcular el total de clases para calcular los porcentajes

    # Extraer los datos necesarios para el gráfico circular
    materias_data = list(materias_counter.values())
    materias_labels = list(materias_counter.keys())
    porcentajes = [round((cantidad / total_clases) * 100, 2) for cantidad in materias_data]

    # Crear y dibujar el gráfico circular
    drawing = Drawing(200, 150)
    pie = Pie()
    pie.x = 60
    pie.y = 60
    pie.width = 120
    pie.height = 120
    pie.data = materias_data
    pie.labels = [f"{label} ({porcentaje} %)" for label, porcentaje in zip(materias_labels, porcentajes)]
    pie.sideLabels = True
    pie.slices.strokeWidth = 0.5
    pie.slices.strokeColor = colors.white
    for i in range(len(materias_labels)):
        pie.slices[i].fillColor = light_colors[i % len(light_colors)]

    drawing.add(pie)
    renderPDF.draw(drawing, p, 70, y - 320)

    # Gráfica de barras (cantidad de clases por día de la semana)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y - 300, "Cantidad de clases por día de la semana")

    # Obtener todas las clases y contarlas por día de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    clases_por_dia = [0] * 7
    for clase in clases:
        dia_semana = clase.fecha_inicio.weekday()
        clases_por_dia[dia_semana] += 1
    
    # Crear y dibujar la gráfica de barras
    drawing = Drawing(200, 150)
    bar = HorizontalBarChart()
    bar.x = 60
    bar.y = 60
    bar.width = 120
    bar.height = 120
    bar.data = [clases_por_dia]
    bar.categoryAxis.categoryNames = dias_semana
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = max(clases_por_dia) + 1

    for i in range(len(dias_semana)):
        bar.bars[i].fillColor = random.choice(light_colors)
    
    drawing.add(bar)
    renderPDF.draw(drawing, p, 350, y - 320)


    p.showPage()
    p.save()

    return response

def export_to_excel(request, codigo_programa):
    programa = Programa.objects.get(codigo=codigo_programa)

    df = pd.DataFrame({
        'Nombre': [programa.nombre],
        # Resto de campos del programa
    })

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="programa.xlsx"'

    df.to_excel(response, index=False)

    return response
