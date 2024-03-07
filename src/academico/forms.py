from django import forms

from .models import Materia

class MateriaForm(forms.Form):
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), empty_label="Seleccionar")