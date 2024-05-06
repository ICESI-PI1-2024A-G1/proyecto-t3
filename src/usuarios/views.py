import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from academico.models import (Clase, Curso, Espacio, EstadoSolicitud, Facultad,
                              MallaCurricular, Materia, Modalidad, Periodo,
                              Programa)
from academico.views import args_principal, verificar_permisos

from .forms import DocenteForm
from .models import (Ciudad, Contrato, Director, Docente, EstadoContrato,
                     EstadoDocente, Persona, TipoContrato, Usuario)

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
            user.usuario.init_groups()
            if user.is_banner:
                return redirect("salones_solicitud")
            return redirect("inicio")
        else:
            messages.error(request, "Usuario y/o contraseña incorrectos. Por favor, inténtelo nuevamente.")

    elif request.user.is_authenticated:
        request.user.usuario.init_groups()
        if request.user.is_banner:
            return redirect("salones_solicitud")
        return redirect("inicio")

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
    return redirect("/")

@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["lideres", "directores"]))
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
    
    request.user.usuario.init_groups()
    
    docentes = Docente.objects.all()
    docente = get_object_or_404(Docente, cedula=cedula)
    periodo = get_object_or_404(Periodo, semestre=periodo)
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
@user_passes_test(lambda u: verificar_permisos(u, ["lideres"]))
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
    
    request.user.usuario.init_groups()
    
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

@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_superuser)
def administrador(request):
    """
    Vista que permite la visualización y gestión de usuarios del sistema.
    Abarca las funcionalidades de creación, edición y eliminación de usuarios.
    Así como la asignación y eliminación de roles a usuarios.
    
    Args:
        request (HttpRequest): La solicitud HTTP recibida.
    
    Returns:
        HttpResponse: La respuesta HTTP que contiene la página de administrador.
    """
    ciudades = Ciudad.objects.all()
    request.user.usuario.init_groups()

    query = request.GET.get("q", None)
    ordenar_por = request.GET.get("ordenar_por", None)
    rol = request.GET.get("rol", None)
    estado = request.GET.get("estado", None)
    users = User.objects.all().order_by("is_active", "first_name", "last_name").exclude(username=request.user.username).exclude(is_superuser=True).exclude(groups__name="banner")
    
    for user in users:
        user.usuario.init_groups()
        user.persona = user.usuario.persona
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    
    if ordenar_por:
        users = users.order_by(ordenar_por)
    
    if rol:
        users = users.filter(groups__id=rol)
    
    if estado:
        users = users.filter(is_active=estado)
    
    return render(
        request,
        "administrador.html",
        {
            "usuarios": users,
            "roles": Group.objects.all().exclude(name="directores").exclude(name="banner"),
            "estados": [True, False],
            "side": "sidebar_principal.html",
            "side_args": args_principal(request.user, "administrador"),
            'ciudades': 'crear-usuario.html', 'ciudades': ciudades,
        },
    )

@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_superuser)
def change_state(request, username):
    """
    Vista que permite cambiar el estado de un usuario (activo/inactivo).

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        username (str): El nombre de usuario del usuario a modificar.

    Returns:
        HttpResponse: Una redirección a la página de administrador.
    """
    if username != request.user.username:
        user_to_change = get_object_or_404(User, username=username)
        user_to_change.is_active = not user_to_change.is_active
        user_to_change.save()
    return redirect("administrador")


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_superuser)
def change_rol(request, username, rol):
    """
    Vista que permite cambiar el rol de un usuario.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        username (str): El nombre de usuario del usuario a modificar.

    Returns:
        HttpResponse: Una redirección a la página de administrador.
    """
    if username != request.user.username:
        user_to_change = get_object_or_404(User, username=username)
        user_to_change.usuario.init_groups()
        if rol:
            user_to_change.groups.clear()
            if rol == "Gestor" and (not user_to_change.is_gestor or user_to_change.is_lider):
                user_to_change.groups.add(Group.objects.get(name="gestores"))

            if rol == "Lider" and not user_to_change.is_lider:
                user_to_change.groups.add(Group.objects.get(name="gestores"))
                user_to_change.groups.add(Group.objects.get(name="lideres"))

            if user_to_change.rol_principal == "Director":
                user_to_change.groups.add(Group.objects.get(name="directores"))
    return redirect("administrador")


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):
    request.user.usuario.init_groups()

    if request.method == 'POST':
        cedula = request.POST['cedula']
        username = request.POST['cedula']
        first_name = request.POST['nombre']
        last_name = request.POST['apellido']
        email = request.POST['email']
        telefono = request.POST['telefono']
        ciudad_id = request.POST['ciudad']
        birthdate = datetime.strptime(request.POST['birthdate'], "%Y-%m-%d") 
        rol = request.POST['rol']

        ciudad = Ciudad.objects.get(id=ciudad_id)
        group = Group.objects.get(name=rol)

        try:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=username)
            fullname = first_name + " " + last_name
            user.groups.add(group)
            user.save()
            if rol == "lideres":
                user.groups.add(Group.objects.get(name="gestores"))
            
            if Persona.objects.filter(cedula=cedula).exists():
                persona = Persona.objects.get(cedula=cedula)
                persona.nombre = fullname
                persona.telefono = telefono
                persona.email = email
                persona.ciudad = ciudad
                persona.fechaNacimiento = birthdate
                persona.save()
            else:
                persona = Persona.objects.create(cedula=cedula, nombre=fullname, email=email, telefono=telefono, ciudad=ciudad, fechaNacimiento=birthdate)
            
            Usuario.objects.create(usuario=user, persona=persona)
        
        except IntegrityError:
            messages.error(request, "Ya existe un usuario con la cédula ingresada.")
            return redirect('/administrador')
        
        return redirect('/administrador')
    else:
        ciudades = Ciudad.objects.all()
        roles = Group.objects.all()
        return redirect('/administrador')
