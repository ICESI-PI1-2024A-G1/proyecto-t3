from django import forms

from .models import Materia
from .models import Periodo

class MateriaForm(forms.Form):
    """
    A form for selecting a Materia and Periodo.

    This form allows the user to select a Materia and Periodo from the available choices.

    Attributes:
        materia (ModelChoiceField): A field for selecting a Materia object.
        periodo (ModelChoiceField): A field for selecting a Periodo object.
    """
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), empty_label="Seleccionar")
    periodo = forms.ModelChoiceField(queryset=Periodo.objects.all(), empty_label="Seleccionar")
