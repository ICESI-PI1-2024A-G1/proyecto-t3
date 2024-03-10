from django import forms

from .models import Docente

class DocenteForm(forms.Form):
    materia = forms.ModelChoiceField(queryset=Docente.objects.all(), empty_label="Seleccionar")