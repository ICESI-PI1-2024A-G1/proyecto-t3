from datetime import datetime
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from academico.views import args_principal
from academico.models import (Clase, Curso, Espacio, EstadoSolicitud, Facultad,
                     MallaCurricular, Materia, Modalidad, Periodo, Programa, EspacioClase)
from solicitud.models import (Solicitud,EstadoSolicitud,SolicitudEspacio,SolicitudClases)

from .models import *
from academico.views import visualizacion_curso

@login_required(login_url="/login")
def solicitud_viaticos(request):
    docentes = Docente.objects.all()
    propositos = PropositoViaje.objects.all()
    if request.method == "POST":
        docenteSeleccionado = request.POST.get("docente_elegido", None)
        fechaIda= datetime.strptime(request.POST.get("ida"), "%Y-%m-%dT%H:%M")
        fechaVuelta= datetime.strptime(request.POST.get("vuelta"), "%Y-%m-%dT%H:%M")
        propositoSeleccionado = request.POST.get("propositoViaje", None)
        descripcion = request.POST.get("desc")
        tiqueteRespuesta = request.POST.get("tiquetes", None)
        alimentacionRespuesta = request.POST.get("alimentacion", None)
        hospedajeRespuesta = request.POST.get("hospedaje", None)
        docente = Docente.objects.get(cedula=docenteSeleccionado)
        propositoViaje = PropositoViaje.objects.get(id=propositoSeleccionado)
        tiquetes = True
        alimentacion = True
        hospedaje = True
        if(tiqueteRespuesta == "No"):
            tiquetes = False
        if(alimentacionRespuesta == "No"):
            alimentacion = False
        if(hospedajeRespuesta == "No"):
            hospedaje = False

        viatico = SolicitudViatico.objects.create(
            descripcion = descripcion,
            fecha_solicitud = datetime.now(),
            docente = docente,
            fecha_ida = fechaIda,
            fecha_vuelta = fechaVuelta,
            propositoViaje = propositoViaje,
            tiquete = tiquetes,
            hospedaje = hospedaje,
            alimentacion = alimentacion
        )
        return redirect("programas")

    return render(
        request,
        "crearViatico.html",
        {
            "docentes": docentes,
            "propositos": propositos,
            "side": "sidebar_crearViatico.html"
        }
    )
    
@login_required(login_url="/login")
def salones_solicitud(request):
    request.user.usuario.init_groups()
    solicitudespendientes = SolicitudEspacio.objects.exclude(estado=2).exclude(estado=3)
    solicitudesaceptadas = SolicitudEspacio.objects.filter(estado=2)
    solicitudesnegadas = SolicitudEspacio.objects.filter(estado=3)
    espaciosclase = EspacioClase.objects.all()



    return render(
        request,
        "salones_solicitud.html",
        {
            "side": "sidebar_principal.html",
            "side_args": args_principal(request.user,"solicitud_clase"),
            "solicitudespacios": solicitudespendientes,
            "solicitudesaceptadas": solicitudesaceptadas,
            "solicitudesnegadas": solicitudesnegadas,
            "espaciosclase": espaciosclase
        }
    )

@login_required(login_url="/login")
def asignar_espacio(request, solicitud_id):
    espacio_id = request.POST.get('espacio_asignado')
    solicitud = get_object_or_404(SolicitudEspacio, id=solicitud_id)
    espacio = get_object_or_404(EspacioClase, id=espacio_id)

    # Obtenemos todas las SolicitudClases asociadas con la SolicitudEspacio
    solicitudclases = SolicitudClases.objects.filter(solicitud=solicitud)

    # Para cada SolicitudClases, asignamos el EspacioClase a la Clase asociada
    for solicitudclase in solicitudclases:
        clase = solicitudclase.clase
        clase.espacio_asignado = espacio
        clase.save()
    estado_aceptado = EstadoSolicitud.objects.get(estado=2)
    solicitud.estado = estado_aceptado
    solicitud.save()

    return redirect('salones_solicitud')

@login_required(login_url="/login")
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudEspacio, id=solicitud_id)
    
    estado_rechazado = EstadoSolicitud.objects.get(estado=3)
    solicitud.estado = estado_rechazado
    solicitud.save()
    return redirect('salones_solicitud')
@login_required(login_url="/login")
def viaticos(request):
        """
    Vista para mostrar la lista de docentes de posgrado.

    Esta vista permite realizar búsquedas y filtrados en la lista de docentes de posgrado.
    Los docentes se pueden filtrar por estado, tipo de contrato y se pueden ordenar por diferentes criterios.
    Además, se implementa la paginación para mostrar los docentes de forma organizada.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP que contiene la página de docentes de posgrado.

    Raises:
        None
    """
    
        request.user.usuario.init_groups()
    
        viaticos = SolicitudViatico.objects.all()

        # Búsqueda y filtrado
        if request.method == "GET":
            query = request.GET.get("q", None)
            query2 = request.GET.get("q2", None)
            tiquete = request.GET.get("tiquete", None)
            hospedaje = request.GET.get("hospedaje", None)
            alimentacion = request.GET.get("alimentacion", None)
            ordenar_por = request.GET.get("ordenar_por", None)

            if query:
                viaticos = viaticos.filter(
                    Q(clase__id__icontains=query)
                )
            if query2:
                viaticos = viaticos.filter(
                    Q(fecha_solicitud= query2)
                )

            if tiquete:
                viaticos = viaticos.filter(tiquete=tiquete)
            if hospedaje:
                viaticos = viaticos.filter(hospedaje=hospedaje)
            if alimentacion:
                viaticos = viaticos.filter(alimentacion=alimentacion)

            if ordenar_por:
                viaticos = viaticos.order_by(ordenar_por)

        paginator = Paginator(viaticos, 10) 

        #Paginación
    
        page_number = request.GET.get('page')
        try:
            viaticos = paginator.page(page_number)
        except PageNotAnInteger:
            viaticos = paginator.page(1)
        except EmptyPage:
            viaticos = paginator.page(paginator.num_pages)

        return render(
            request,
            "viaticos.html",
            {
                "viaticos": viaticos,
                "side": "sidebar_principal.html",
                "side_args": args_principal(request.user,"viaticos"),
            },
        )
