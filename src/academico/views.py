from django.shortcuts import render

from .forms import MateriaForm

# Create your views here.

def crear_curso(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            # Aquí se guardará el curso en la base de datos
            pass
    else:
        form = MateriaForm()

    return render(request, 'crear-curso.html', {'form': form})