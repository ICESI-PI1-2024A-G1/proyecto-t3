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

# Create your views here.
