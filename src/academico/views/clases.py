from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from academico.models import (Clase, Curso, Docente, Espacio, Estudiante,
                              GrupoDeClase, Modalidad)
from ccsa_project import settings


@login_required(login_url="/login")
def solicitar_salones(request, curso_id):
    """
    Vista que permite solicitar salones para las clases de un curso.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP que muestra la página de solicitud de salones.
    """
    curso = get_object_or_404(Curso, nrc=curso_id)
    # Solicitud.objects.create(curso=curso, tipo="Salones")


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
        num_semanas_str = request.POST.get("num_semanas", "1")
        num_semanas = 1 if num_semanas_str == "" else int(num_semanas_str)
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

        grupo_clases = GrupoDeClase.objects.create()

        for _ in range(num_semanas):
            clase = Clase.objects.create(
                fecha_inicio=start_day,
                fecha_fin=end_day,
                espacio_asignado=None,
                curso_id=curso_id,
                espacio_id=tipo_espacio,
                modalidad_id=modalidad_clase,
                docente=docente,
                grupo_clases=grupo_clases,
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
    clase = get_object_or_404(Clase, id=clase_id)
    if request.method == "POST":
        fecha_inicio = datetime.strptime(
            request.POST.get("fecha_inicio"), "%Y-%m-%dT%H:%M"
        )
        fecha_fin = datetime.strptime(request.POST.get("fecha_fin"), "%Y-%m-%dT%H:%M")
        tipo_espacio_id = request.POST.get("tipo_espacio_e")
        modalidad_id = request.POST.get("modalidad_clase_e")
        docente_cedula = request.POST.get("docente_clase_e")
        editar_relacionadas = request.POST.get("editar_relacionadas_e")

        if (
            fecha_inicio == None
            or fecha_fin == None
            or tipo_espacio_id == None
            or modalidad_id == None
        ):
            raise Http404("Todos los campos son requeridos.")

        try:
            tipo_espacio = Espacio.objects.get(id=tipo_espacio_id)
        except Espacio.DoesNotExist:
            raise Http404("Tipo de espacio no existe.")

        try:
            modalidad = Modalidad.objects.get(id=modalidad_id)
        except Modalidad.DoesNotExist:
            raise Http404("Modalidad no existe.")

        if docente_cedula is not None and docente_cedula != "None":
            try:
                docente = Docente.objects.get(cedula=docente_cedula)

            except Docente.DoesNotExist:
                raise Http404("Docente no existe.")
        else:
            docente = None

        old_date = clase.fecha_inicio

        clase.fecha_inicio = fecha_inicio
        clase.fecha_fin = fecha_fin
        clase.espacio = tipo_espacio
        clase.modalidad = modalidad
        clase.docente = docente
        clase.save()

        if editar_relacionadas:
            for clase_i in Clase.objects.filter(grupo_clases=clase.grupo_clases):
                clase.fecha_inicio
                if clase_i.fecha_inicio > old_date:
                    fecha_inicio += timedelta(days=7)
                    fecha_fin += timedelta(days=7)
                    clase_i.fecha_inicio = fecha_inicio
                    clase_i.fecha_fin = fecha_fin
                    clase_i.espacio = tipo_espacio
                    clase_i.modalidad = modalidad
                    clase_i.docente = docente
                    clase_i.save()

        # Estudiantes
        estudiantes = Estudiante.objects.filter(cursos=clase.curso)
        to_email = []  # List of recipients
        for es in estudiantes:
            to_email.append(es.email)
        # Extracting just the date part from the datetime objects
        fecha_inicio_str = clase.fecha_inicio.date()

        # Extracting just the time part from the datetime objects
        hora_inicio_str = clase.fecha_inicio.time()
        hora_fin_str = clase.fecha_fin.time()

        subject = f"{clase.id} class change"

        if clase.docente is not None:
            nombre_docente = clase.docente.nombre
            to_email.append(clase.docente.email)  # List of recipients
        else:
            nombre_docente = "N/A"

        # Rendering the message using an HTML template
        html_message = render_to_string(
            "email_template.html",
            {
                "fecha_inicio": fecha_inicio_str,
                "tipo_espacio": clase.espacio.tipo,
                "espacio_asignado": clase.espacio_asignado,
                "metodologia": clase.modalidad.metodologia,
                "nombre_docente": nombre_docente,
                "hora_inicio": hora_inicio_str,
                "hora_fin": hora_fin_str,
            },
        )

        from_email = settings.EMAIL_HOST_USER

        # Sending the email with both plain text and HTML content
        if to_email is not None:
            send_mail(
                subject, html_message, from_email, to_email, html_message=html_message
            )

    return redirect("visualizar-curso", curso_id=clase.curso.nrc)


# Create your views here.


@login_required(login_url="/login")
@require_POST
def eliminar_clase(request, clase_id):
    """
    Elimina una clase del sistema.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        clase_id (int): El ID de la clase a eliminar.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización del curso al que pertenecía la clase.
    """
    if request.method == "POST":
        clase = get_object_or_404(Clase, id=clase_id)
        clase.delete()

        return redirect("visualizar-curso", curso_id=clase.curso.nrc)
