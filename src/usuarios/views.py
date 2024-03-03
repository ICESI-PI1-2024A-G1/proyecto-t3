from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

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
