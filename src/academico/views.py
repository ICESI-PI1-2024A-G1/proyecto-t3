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

from .models import Materia
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