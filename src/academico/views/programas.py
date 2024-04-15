import io
import json
from datetime import datetime, timedelta

import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa

from academico.models import (Clase, Curso, Docente, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Periodo, Programa)
from ccsa_project import settings

from .common import args_principal, color_suave, obtener_modalidad


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
    programa = get_object_or_404(Programa, codigo=codigo)
    materias = MallaCurricular.objects.filter(
        programa__codigo=codigo, periodo__semestre=periodo
    )

    malla_curricular = {}
    tamaño = 0
    creditos_totales = 0
    cursos_totales = 0
    docentes_con_clase = []
    programa.total_grupos = len(
        Curso.objects.filter(
            periodo__semestre=periodo, materia__programas__codigo=codigo
        ).distinct()
    )
    programa.total_clases_docente = len(
        Clase.objects.filter(
            curso__materia__programas__codigo=codigo,
            curso__periodo__semestre=periodo,
            docente__isnull=False,
        ).distinct()
    )
    programa.total_clases = len(
        Clase.objects.filter(
            curso__materia__programas__codigo=codigo, curso__periodo__semestre=periodo
        ).distinct()
    )
    programa.porcentaje_clases_docente = int(
        (programa.total_clases_docente / programa.total_clases) * 100
        if programa.total_clases > 0
        else 0
    )
    programa.lista_materias = "Materias del pensum:\n\n"

    programa.lista_cursos_incompletos = Curso.objects.filter(
        periodo__semestre=periodo,
        materia__programas__codigo=codigo,
        clase__docente__isnull=True,
    ).distinct()
    programa.cursos_incompletos = "Cursos incompletos:\n\n"
    for curso in programa.lista_cursos_incompletos:
        programa.cursos_incompletos += f"{curso.materia.nombre} - Grupo {curso.grupo}\n"

    for materia in materias:
        programa.lista_materias += (
            f"{materia.materia.nombre} - Semestre {materia.semestre}\n"
        )
        materia.materia.color = color_suave()
        creditos_totales += materia.materia.creditos
        cursos_totales += 1
        docentes_con_clase += Docente.objects.filter(
            clase__curso__materia=materia.materia,
            clase__curso__periodo__semestre=periodo,
        ).distinct()
        if materia.semestre not in malla_curricular.keys():
            tamaño = 1
            malla_curricular[materia.semestre] = []
        malla_curricular[materia.semestre].append(materia.materia)

    semestres = len(malla_curricular.keys())

    docentes = set()
    for docente in docentes_con_clase:
        docente.lista_materias = Materia.objects.filter(
            curso__clase__docente=docente
        ).distinct()
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


@login_required(login_url="/login")
def primera_clase_programa(request, codigo, periodo):
    """
    Obtiene la primera clase de un programa académico para un periodo específico.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        codigo (str): El código del programa académico.
        periodo (str): El periodo para el cual se obtendrá la primera clase.

    Returns:
        JsonResponse: Un JSON con la información de la primera clase del programa académico.
    """

    clases = Clase.objects.filter(
        curso__periodo__semestre=periodo, curso__materia__programas__codigo=codigo
    ).distinct()
    primera_clase = None

    for clase in clases:
        if not primera_clase or clase.fecha_inicio < primera_clase.fecha_inicio:
            primera_clase = clase

    if primera_clase:
        return JsonResponse(
            {
                "curso": primera_clase.curso.materia.nombre,
                "fecha_inicio": primera_clase.fecha_inicio,
                "fecha_fin": primera_clase.fecha_fin,
                "espacio": primera_clase.espacio.tipo,
                "modalidad": primera_clase.modalidad.metodologia,
                "total_clases": len(clases),
            }
        )
    return JsonResponse({"total_clases": len(clases)})


def render_pdf(html_content):
    """
    Renderiza HTML como PDF y devuelve un objeto HttpResponse con el PDF.
    """
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    print(pdf.err)
    return None


@login_required(login_url="/login")
def enviar_para_aprobacion(request, codigo, periodo):
    """
    Envía una solicitud de aprobación de un programa académico.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        codigo (str): El código del programa académico.
        periodo (str): El periodo para el cual se enviará la solicitud de aprobación.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del programa académico.
    """
    try:
        if request.method == "POST":
            body = json.loads(request.body.decode("utf-8"))
            programa = get_object_or_404(Programa, codigo=codigo)

            # Generar el PDF
            template = get_template("programa_pdf.html")
            pdf_content = render_pdf(
                template.render(export_program_data(codigo, periodo))
            )

            html_content = get_template("aprobacion_email.html").render(
                {
                    "programa": programa,
                    "comentarios": (
                        body["comentarios"].replace("&nbsp;", " ").split("<br>")
                        if "<br>" in body["comentarios"]
                        else [body["comentarios"]]
                    ),
                    "url": request.build_absolute_uri(
                        reverse(
                            "programa", kwargs={"codigo": codigo, "periodo": periodo}
                        )
                    ),
                }
            )
            if pdf_content:
                # Crear el correo electrónico
                subject = f"REVISIÓN DEL PROGRAMA - {programa.nombre}"
                message = body["comentarios"]
                from_email = settings.EMAIL_HOST_USER
                to_email = [programa.director.email]

                # Adjuntar el PDF al correo electrónico
                email = EmailMultiAlternatives(subject, message, from_email, to_email)
                email.attach_alternative(html_content, "text/html")
                email.attach("programa.pdf", pdf_content, "application/pdf")

                # Enviar el correo electrónico
                email.send()

                # Actualizar el estado del programa
                programa.estado_solicitud = EstadoSolicitud.objects.get(
                    nombre="Por aprobar"
                )
                programa.save()

        return redirect("programa", codigo=codigo, periodo=periodo)
    except Exception as e:
        raise Http404("Error al enviar la solicitud de aprobación.")


@login_required(login_url="/login")
def importar_malla(request, codigo, periodo):
    """
    Importa una malla curricular desde un periodo anterior al periodo actual.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        codigo (str): El código del programa académico.
        periodo (str): El periodo actual.

    Returns:
        JsonResponse: Un objeto JSON con un mensaje de éxito si la malla curricular se importó correctamente,
        o un objeto JSON con un mensaje de error si ocurrió un error al importar la malla curricular.
    """
    body = json.loads(request.body.decode("utf-8"))

    primera_clase_actual = datetime.strptime(
        body.get("primera_clase_actual"), "%Y-%m-%d"
    )
    primera_clase_importar = datetime.strptime(
        body.get("primera_clase_importar"), "%Y-%m-%dT%H:%M:%SZ"
    )
    delta = (primera_clase_actual - primera_clase_importar).days
    if delta % 7 != 0:
        delta += 1
    incluir_docentes = body.get("incluir_docentes")
    periodo_importar = body.get("periodo_importar").split("/")[1]

    MallaCurricular.objects.filter(
        programa__codigo=codigo, periodo__semestre=periodo
    ).delete()

    try:
        for malla_anterior in MallaCurricular.objects.filter(
            programa__codigo=codigo, periodo__semestre=periodo_importar
        ).distinct():
            MallaCurricular.objects.create(
                materia=malla_anterior.materia,
                programa=malla_anterior.programa,
                periodo=Periodo.objects.get(semestre=periodo),
                semestre=malla_anterior.semestre,
            )
            Curso.objects.filter(
                materia=malla_anterior.materia, periodo__semestre=periodo
            ).distinct().delete()
            for curso_anterior in Curso.objects.filter(
                materia=malla_anterior.materia, periodo=malla_anterior.periodo
            ).distinct():
                curso = Curso.objects.create(
                    cupo=curso_anterior.cupo,
                    grupo=curso_anterior.grupo,
                    materia=curso_anterior.materia,
                    periodo=Periodo.objects.get(semestre=periodo),
                )
                for clase_anterior in (
                    Clase.objects.filter(curso=curso_anterior)
                    .distinct()
                    .order_by("fecha_inicio")
                ):
                    Clase.objects.create(
                        fecha_inicio=clase_anterior.fecha_inicio
                        + timedelta(days=delta),
                        fecha_fin=clase_anterior.fecha_fin + timedelta(days=delta),
                        espacio=clase_anterior.espacio,
                        curso=curso,
                        modalidad=clase_anterior.modalidad,
                        docente=clase_anterior.docente if incluir_docentes else None,
                    )
    except:
        return JsonResponse({"error": "Error al importar la malla curricular."})
    return JsonResponse({"success": "Malla curricular importada exitosamente."})


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
    body = json.loads(request.body.decode("utf-8"))
    for key in body:
        if (
            len(
                MallaCurricular.objects.filter(
                    programa__codigo=codigo, periodo__semestre=periodo
                )
            )
            < 1
        ):
            continue
        if MallaCurricular.objects.filter(
            materia__codigo=key, programa__codigo=codigo, periodo__semestre=periodo
        ).exists():
            malla = MallaCurricular.objects.get(
                materia__codigo=key, programa__codigo=codigo, periodo__semestre=periodo
            )
            malla.semestre = body[key]
            malla.save()
    return redirect("programa", codigo=codigo, periodo=periodo)


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
    programa = get_object_or_404(Programa, codigo=codigo)
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


def render_pdf_from_html(html_content):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="programa.pdf"'

    # Renderizar el HTML como PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    # Si ocurrió un error, mostrarlo
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err, status=500)
    return response

def export_program_data(codigo_programa, periodo):
    pensum = {}
    docentes_con_clase = []
    materias = []
    cursos_totales = 0
    creditos_totales = 0
    programa = get_object_or_404(Programa, codigo=codigo_programa)
    programa.modalidad = obtener_modalidad(MallaCurricular.objects.filter(programa__codigo=codigo_programa, periodo__semestre=periodo))
    malla_curricular = MallaCurricular.objects.filter(programa__codigo=codigo_programa, periodo__semestre=periodo)

    for malla in malla_curricular: 
        materia = malla.materia
        materia.num_clases = 0 
        materia.num_clases_asignadas = 0
        materia.num_cursos = 0
        materias.append(materia)
        cursos_totales += 1
        creditos_totales += materia.creditos
        materia.cursos = Curso.objects.filter(materia=materia, periodo__semestre=periodo)
        docentes_con_clase+=Docente.objects.filter(clase__curso__materia=malla.materia, clase__curso__periodo__semestre=periodo).distinct()
        if malla.semestre not in pensum.keys():
            pensum[malla.semestre] = []
        pensum[malla.semestre].append(materia)
        for curso in materia.cursos:
            materia.num_cursos += 1
            curso.clases = Clase.objects.filter(curso=curso)
            curso.num_clases = len(curso.clases)
            materia.num_clases += curso.num_clases
            materia.num_clases_asignadas += len(Clase.objects.filter(curso=curso, docente__isnull=False))

    programa.creditos = sum([materia.creditos for materia in materias])
    programa.cursos_totales = cursos_totales
    programa.docentes = docentes_con_clase
    programa.creditos_totales = creditos_totales
    programa.pensum = pensum

    docentes = set()
    for docente in docentes_con_clase:
        docente.lista_materias = Materia.objects.filter(curso__clase__docente=docente).distinct()
        docentes.add(docente)

    return {
        "programa": programa,
        "periodo": periodo,
        "materias": materias,
        "docentes": docentes,
    }


def export_to_pdf(request, codigo_programa, periodo):
    template = get_template('programa_pdf.html')
    html_content = template.render(export_program_data(codigo_programa, periodo))

    return render_pdf_from_html(html_content)

def export_to_excel(request, codigo_programa, periodo):
    programa = get_object_or_404(Programa, codigo=codigo_programa)
    clases = []
    total_horas_programadas = timedelta()

    for malla in MallaCurricular.objects.filter(programa__codigo=codigo_programa, periodo__semestre=periodo): 
        for curso in Curso.objects.filter(materia=malla.materia, periodo__semestre=periodo):
            for clase in  Clase.objects.filter(curso=curso):
                clase.programa = programa
                clase.materia = malla.materia
                clase.periodo = malla.periodo
                clase.facultad = programa.facultad
                clase.horas_programadas = clase.fecha_fin - clase.fecha_inicio
                total_horas_programadas += clase.horas_programadas
                clase.total_horas_programadas = total_horas_programadas
                clases.append(clase)
    data = {
        'Código_Facultad': [],
        'Nombre_Facultad': [],
        'Código_Programa': [],
        'Nombre_Programa': [],
        'Código_Materia': [],
        'Nombre_Materia': [],
        'NRC': [],
        'Grupo': [],
        'Método_Educativo': [],
        'Cupo_Materia': [],
        'Número_Horas': [],
        'Horas_Programadas': [],
        "Número_Créditos": [],
        "Cédula": [],
        "Nombre_Profesor": [],
        "Código_Contrato": [],
        "Tipo_Contrato": [], 
        "Fecha_Contrato": [],
        "Estado_Contrato": [],
        "Fecha_Inicio": [],
        "Fecha_Fin": [], 
        "HR_Inicio": [],
        "HR_Fin": [],
        "Espacio": [],

    }
    
    for clase in clases:
        data["Código_Facultad"].append(clase.facultad.id)
        data["Nombre_Facultad"].append(clase.facultad.nombre)
        data["Código_Programa"].append(clase.programa.codigo)
        data["Nombre_Programa"].append(clase.programa.nombre)
        data["Código_Materia"].append(clase.materia.codigo)
        data["Nombre_Materia"].append(clase.materia.nombre)
        data["NRC"].append(clase.curso.nrc)
        data["Grupo"].append(clase.curso.grupo)
        data["Método_Educativo"].append(clase.modalidad.metodologia)
        data["Cupo_Materia"].append(clase.curso.cupo)
        data["Número_Horas"].append(clase.horas_programadas)
        data["Horas_Programadas"].append(clase.total_horas_programadas)
        data["Número_Créditos"].append(clase.materia.creditos),
        data["Cédula"].append(clase.docente.cedula if clase.docente else "No asignado")
        data["Nombre_Profesor"].append(clase.docente.nombre if clase.docente else "No asignado")
        data["Código_Contrato"].append(clase.docente.contrato_codigo.codigo if clase.docente else "")
        data["Tipo_Contrato"].append(clase.docente.contrato_codigo.tipo_contrato.tipo if clase.docente else "-")
        data["Fecha_Contrato"].append(clase.docente.contrato_codigo.fecha_elaboracion if clase.docente else "-")
        data["Estado_Contrato"].append(clase.docente.contrato_codigo.estado.estado if clase.docente else "-")
        data["Fecha_Inicio"].append(clase.fecha_inicio.replace(tzinfo=None).strftime("%Y-%m-%d") if clase.fecha_inicio else "-")
        data["Fecha_Fin"].append(clase.fecha_fin.replace(tzinfo=None).strftime("%Y-%m-%d") if clase.fecha_fin else "-") 
        data["HR_Inicio"].append(clase.fecha_inicio.replace(tzinfo=None).strftime("%H:%M") if clase.fecha_inicio else "-")
        data["HR_Fin"].append(clase.fecha_fin.replace(tzinfo=None).strftime("%H:%M") if clase.fecha_fin else "-") 
        data["Espacio"].append(clase.espacio_asignado.id if clase.espacio_asignado else "No asignado")


    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="programa.xlsx"'

    df.to_excel(response, index=False)

    return response