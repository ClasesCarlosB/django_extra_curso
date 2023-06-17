from django import forms
from django.forms import ModelForm
from .models import Curso

class FormularioCurso(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=128)
    inscriptos = forms.IntegerField(label="Inscriptos")
    """
    solo_empresas = forms.BooleanField(label="¿Solo empresas?", required=False)
    TURNOS = (
        (1, "Mañana"),
        (2, "Tarde"),
        (3, "Noche"))
    turno = forms.ChoiceField(label="Turno", choices=TURNOS)
    fecha_inicio = forms.DateField(
        label="Fecha de inicio",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(attrs={"type": "date"})
    )
    """

class FormularioCursoDos(ModelForm):
    class Meta:
        model = Curso
        fields = ["nombre", "inscriptos","turno"]
        