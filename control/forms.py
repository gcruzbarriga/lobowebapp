from django import forms
from django.forms import ModelForm
from control.models import Personal, ControlHoras


class PersonalForm(ModelForm):
    class Meta:
        model = Personal
        fields = '__all__'
#         model.fecha_nac = DateField(input_formats=['%d/%m/%Y'])
#         Ejemplos de como jalar los datos de los modelos

#         fields = '__all__'
#         fields = ("nombre",
#                     "apellidoPat",
#                     "apellidoMat",
#                     "fechaNac")

class ControlHorasForm(ModelForm):
    class Meta:
        model = ControlHoras
        #fields = '__all__'
        exclude = ["trabajador"
                   ]