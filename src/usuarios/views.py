import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from academico.models import (Clase, Curso, Espacio, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Modalidad, Periodo,
                              Programa)
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
        user = authenticate(request, username=form['username'], password=form['password'])
        if user is not None:
            login(request, user)
            return redirect("programas")
        else:
            messages.error(request, "Usuario y/o contraseña incorrectos. Por favor, inténtelo nuevamente.")

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

@login_required(login_url="/login")
def docente_Detail(request, cedula, periodo):
    """
    Vista que permite renderizar la pantalla 'docenteProfile.html' con información del docente.
    Además de poder editar el estado del docente.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        cedula (str): La cédula del docente.
        periodo (str): Un periodo academico.

    Returns:
        HttpResponse: La plantilla 'docenteProfile.html' renderizada con las siguientes variables de contexto:
            - 'docente': El objeto Docente.
            - 'periodo_seleccionado': El período seleccionado.
            - 'clasesDocente': Las clases relacionados con el docete y el periodo especificado
            - 'dias': Lista de días necesaria para crear los días de la semana en el horario de clases del docente.
            - 'periodos': Todos los objetos Periodo.
            - 'estados': Todos los objetos EstadoDocente.
            - 'side': La plantilla de la barra lateral a incluir.

    Raises:
        Http404: Si no se encuentra el docente con el código especificado.
    """
    docentes = Docente.objects.all()
    docente = get_object_or_404(Docente, cedula=cedula)
    estados = EstadoDocente.objects.all()
    if request.method == "POST":
        id_nuevo_estado = request.POST.get('nuevoEstado',None)

        # Busca el nuevo estado en la base de datos
        nuevo_estado = EstadoDocente.objects.get(id=id_nuevo_estado)

        if(nuevo_estado == docente.estado):
            return redirect("ver_docente", cedula=cedula, periodo = periodo)

        docente.estado = nuevo_estado
        docente.save()
    
    clasesDocente = Clase.objects.filter(docente=docente , curso__periodo=periodo)
    clasesDocenteOrdenada = Clase.objects.filter(docente=docente , curso__periodo=periodo).order_by("fecha_inicio")

    dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = traducir(dias)
    #en cada iteración del bucle, dia será un día en inglés y day será su traducción al español.
    dias_days = zip(dias, days)
    return render(
        request,
        "docenteProfile.html", 
        {
            'docente': docente,
            'periodo_seleccionado': periodo,
            'clasesDocente': clasesDocente,
            'clasesDocenteOrdenada': clasesDocenteOrdenada,
            'dias': dias,
            'dias_days':dias_days ,
            'periodos': Periodo.objects.all(),
            'estados': estados,
            "side": "sidebar_docente.html"
        },
    )

def traducir(dias):
    """
    Función que va a agregando cada día de la lista de dias (en inglés), traducido al español, en una lista de dias traducidos.

    Args:
        dias: Lista con los días en inglés.

    Returns: Una lista de días traducidos
        
    """
    dias_traducidos = []
    for dia in dias:
        day = traducir_a_español(dia)
        dias_traducidos.append(day)
    return dias_traducidos


def traducir_a_español(dia):
    """
    Función que va traduce el día especificado según su valor.

    Args:
        dia: dia en ingles

    Returns: un día con su traducción equivalente
        
    """
    dias_semana = {
        'Monday':'Lunes',
        'Tuesday':'Martes',
        'Wednesday':'Miércoles',
        'Thursday':'Jueves',
        'Friday':'Viernes',
        'Saturday':'Sábado',
        'Sunday':'Domingo'
    }

    return dias_semana.get(dia, dia)
@login_required(login_url="/login")
def docentes(request):
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
            "side_args": args_principal(request.user,"docentes"),
        },
    )


def error_404(request, exception):
    return render(request, '404.html', status=404)