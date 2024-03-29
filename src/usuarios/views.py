import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from academico.views import args_principal

from .forms import DocenteForm
from .models import (Ciudad, Contrato, Director, Docente, EstadoContrato,
                     EstadoDocente, Persona, TipoContrato)

# Create your views here.

def login_page(request):
    """
    Vista que maneja la página de inicio de sesión.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP que se enviará al cliente.
    """
    if request.method == 'POST':
        form = request.POST
        login(request, authenticate(request, username=form['username'], password=form['password']))
        if request.user.is_authenticated:
            return redirect("programas")

    elif request.user.is_authenticated:
        return redirect('programas')

    return render(request, 'login.html', {
        'form': AuthenticationForm
    })

def log_out(request):
    """
    Cierra la sesión del usuario actual.

    Args:
        request: La solicitud HTTP recibida.

    Returns:
        Una redirección a la página de inicio de sesión.
    """
    logout(request)
    return redirect("login")


def docente_Detail(request, cedula):
    if request.method=='GET':
        docente = get_object_or_404(Docente, cedula=cedula)
        return render(request, "docenteProfile.html", {'docente': docente})
    
#@login_required(login_url="/login")
def docentes(request):
    docentes = Docente.objects.all()

    # Búsqueda y filtrado
    if request.method == "GET":
        query = request.GET.get("q", None)
        estado = request.GET.get("estado", None)
        contrato = request.GET.get("contrato", None)
        ordenar_por = request.GET.get("ordenar_por", None)

        if query:
            docentes = docentes.filter(
                Q(nombre__icontains=query)
                | Q(cedula__icontains=query)
            )

        if estado:
            docentes = docentes.filter(estado__id=estado)
        if contrato:
            docentes = docentes.filter(contrato_codigo__tipo_contrato__id=contrato)

        if ordenar_por:
            docentes = docentes.order_by(ordenar_por)

    paginator = Paginator(docentes, 10) 

    #Paginación
    
    page_number = request.GET.get('page')
    try:
        docentes = paginator.page(page_number)
    except PageNotAnInteger:
        docentes = paginator.page(1)
    except EmptyPage:
        docentes = paginator.page(paginator.num_pages)

    estados = EstadoDocente.objects.all()
    contratos = TipoContrato.objects.all()

    return render(
        request,
        "docentes.html",
        {
            "docentes": docentes,
            "estados": estados,
            "contratos": contratos,
            "side": "sidebar_principal.html",
            "side_args": args_principal("docentes"),
        },
    )

