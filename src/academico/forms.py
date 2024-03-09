from django import forms

from .models import Materia
from .models import Periodo

class MateriaForm(forms.Form):
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), empty_label="Seleccionar")
    periodo = forms.ModelChoiceField(queryset=Periodo.objects.all(), empty_label="Seleccionar")
