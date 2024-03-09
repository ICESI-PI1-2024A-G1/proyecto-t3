from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Clase
from django.http import HttpResponse

def crear_clase(request):
    if request.method == 'POST':
        start_day = request.POST('start_day')
        end_day = request.POST('end_day')
        time = request.POST.get('time')
        weeks = request.POST.get('weeks')
        mode = request.POST.get('mode')
        curso_id = request.POST.get('curso_id')

        new_class = Clase(start_day=start_day, end_day=end_day, time=time, weeks=weeks, mode=mode, curso_id=curso_id)
        new_class.save()

        return redirect('visualizar clases')
    else:
        return HttpResponse("Metodo no permitido")

from .forms import MateriaForm

from .models import EstadoSolicitud, Materia, Programa, Facultad
from .models import Periodo

# Create your views here.

def crear_curso(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            # Aquí se guardará el curso en la base de datos
            pass
    else:
        form = MateriaForm()

    materias = Materia.objects.all()
    periodos = Periodo.objects.all()

    return render(request, 'crear-curso.html', {'form': form, 'materias': materias, 'periodos': periodos})

def programas(request):
    programas = Programa.objects.all()
    periodos_academicos = Periodo.objects.all()
    facultades = Facultad.objects.all()
    estados = EstadoSolicitud.objects.all() 

    # Búsqueda y filtrado
    if request.method == 'GET':
        periodo_seleccionado = request.GET.get('periodo', None)
        query = request.GET.get('q', None)
        facultad = request.GET.get('facultad', None)
        estado = request.GET.get('estado', None)
        ordenar_por = request.GET.get('ordenar_por', None)

        if periodo_seleccionado:
            programas = programas.filter(periodo__semestre=periodo_seleccionado)

        if query:
            programas = programas.filter(
                Q(nombre__icontains=query) |
                Q(facultad__nombre__icontains=query) |
                Q(director__nombre__icontains=query) |
                Q(nombre__icontains=query) 
            )

        if facultad:
            programas = programas.filter(facultad__id=facultad)
        if estado:
            programas = programas.filter(estado_solicitud__estado=estado)

        if ordenar_por:
            programas = programas.order_by(ordenar_por)


    return render(request, 'programas.html', {
        'programas': programas,
        'periodos_academicos': periodos_academicos,
        'facultades': facultades,
        'estados': estados,
    })