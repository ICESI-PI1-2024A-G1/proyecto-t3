from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Docente
from django.shortcuts import render, get_object_or_404
from .forms import DocenteForm

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        form = request.POST
        login(request, authenticate(request, username=form['username'], password=form['password']))
        if request.user.is_authenticated:
            return render(request, 'home.html')
        
    return render(request, 'login.html', {
        'form': AuthenticationForm
    })

def log_out(request):
    logout(request)
    return render(request, "login.html", {"form": AuthenticationForm})

def registrar_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = DocenteForm()
    docentes = Docente.objects.all()
    return render(request, 'registrar_docente', {'form': form, 'docentes': docentes})


        

def docente_Detail(request, docente_cedula):
    if request.method=='GET':
        docente = get_object_or_404(Docente, cedula=docente_cedula)
        return render(request, "docenteProfile.html", {'docente': docente})

