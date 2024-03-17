from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from academico.views import programas

from .forms import DocenteForm
from .models import Docente

# Create your views here.

def login_page(request):
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
    logout(request)
    return redirect("login")


def docente_Detail(request, cedula):
    if request.method=='GET':
        docente = get_object_or_404(Docente, cedula=cedula)
        return render(request, "docenteProfile.html", {'docente': docente})
