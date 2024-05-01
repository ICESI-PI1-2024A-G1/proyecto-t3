from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from academico.models import Clase, Curso, Docente, Materia, Periodo, Programa

from .common import args_principal, color_suave, verificar_permisos


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["gestores", "directores"]))
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
    
    request.user.usuario.init_groups()
    
    if request.user.is_director:
        materias = materias.filter(programas__director__cedula=request.user.usuario.persona.cedula)
        programas = programas.filter(director__cedula=request.user.usuario.persona.cedula)
        

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
            "side_args": args_principal(request.user,"materias"),
        },
    )


@login_required(login_url="/login")
@user_passes_test(lambda u: verificar_permisos(u, ["gestores", "directores"]))
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

    request.user.usuario.init_groups()

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
