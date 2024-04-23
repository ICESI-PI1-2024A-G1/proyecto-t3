import random
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from academico.views import args_principal
from usuarios.models import (Ciudad, Contrato, Director, Docente, EstadoContrato,
                     EstadoDocente, Persona, TipoContrato)
from academico.models import (Clase, Curso, Espacio, EstadoSolicitud, Facultad,
                     MallaCurricular, Materia, Modalidad, Periodo, Programa)

from .models import *

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
    
    return render(
        request,
        "salones_solicitud.html",
        {
            "side": "sidebar_principal.html",
            "side_args": args_principal(request.user,"solicitud_clase")
        }
    )

