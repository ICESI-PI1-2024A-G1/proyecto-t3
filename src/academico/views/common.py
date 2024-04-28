import json
import random

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.shortcuts import render

from academico.models import Clase, Materia, Programa
from usuarios.models import Docente


def verificar_permisos(user, roles):
    """
    Valida si el usuario tiene alguno de los roles especificados.

    Args:
        user (User): El usuario a validar.
        roles (list): Lista de roles a validar.

    Returns:
        bool: True si el usuario tiene alguno de los roles especificados, False en caso contrario.
    """
    for rol in roles:
        if user.groups.filter(name=rol).exists():
            return True
    return False

def args_principal(user, seleccionado):
    """
    Genera un diccionario con la información de los menús de la barra lateral del menú principal.

    Args:
        seleccionado (str): El menú seleccionado actualmente.

    Returns:
        dict: Un diccionario con la información de los menús, donde la clave es el nombre del menú y el valor es otro diccionario con la URL y si está seleccionado o no.
    """
    
    sites = {}

    if user.is_gestor or user.is_director:
        sites["Inicio"] = {"url": "/academico/inicio", "seleccionado": seleccionado=="Inicio"}
    
    if user.is_gestor or user.is_director:
        sites["Programas posgrado"] = {"url": "/academico/programas", "seleccionado": seleccionado=="programas"}
    
    if user.is_gestor or user.is_director:
        sites["Materias posgrado"] = {"url": "/academico/materias", "seleccionado": seleccionado=="materias"}
    
    if user.is_lider:
        sites["Docentes posgrado"] = {"url": "/docentes", "seleccionado": seleccionado=="docentes"}
    
    if user.is_gestor:
        sites["Solicitud"] = {"url": "/solicitud/viaticos", "seleccionado": seleccionado=="solicitud"}
    
    if user.is_banner:
        sites["Solicitud de Salones"] = {"url": "/solicitud/salones_solicitud", "seleccionado": seleccionado=="solicitud_clase"}
    
    if user.is_superuser:
        sites["Administrador"] = {"url": "/administrador", "seleccionado": seleccionado=="administrador"}
        
    return sites

def color_suave():
    """
    Retorna un color suave seleccionado aleatoriamente de una lista.
    La lista de colores está definida en el CSS.

    Returns:
        int: Un número entero que representa el color seleccionado.
    """
    color = random.choice([1, 2, 3])
    return color


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


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["gestores", "directores"]))
def inicio(request):

    request.user.usuario.init_groups()
    total_programas = Programa.objects.count()
    total_docentes = Docente.objects.count()
    total_materias = Materia.objects.count()
    total_clases = Clase.objects.count()

    estados_programas = list(Programa.objects.values('estado_solicitud__nombre').annotate(total=Count('estado_solicitud')))
    clases_por_dia = list(Clase.objects.annotate(dia_semana=ExtractWeekDay('fecha_inicio')).values('dia_semana').annotate(total=Count('id')))

    return render(request, "inicio.html", {
        "total_programas": total_programas,
        "total_docentes": total_docentes,
        "total_materias": total_materias,
        "total_clases": total_clases,
        "estados_programas_json": json.dumps(estados_programas),
        "clases_por_dia_json": json.dumps(clases_por_dia),
        "side": "sidebar_principal.html",
        "side_args": args_principal(request.user, "Inicio"),
    },
)

def solicitudes_salones(request):
    return render(request, "salones_solicitud.html", {
        "side": "sidebar_principal.html",
        "side_args": args_principal(request.user, "Solicitud de Salones"),
    }
)
