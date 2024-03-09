from django.shortcuts import render

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