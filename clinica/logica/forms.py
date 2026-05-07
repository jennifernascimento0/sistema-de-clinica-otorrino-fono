from django import forms
from .models import Profissional, Consulta

class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['nome', 'especialidade', 'registro', 'telefone'] #tudo o que quiser que apareça

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'profissional', 'data', 'observacoes']
        widgets = {
            #pra mostrar o calendário do navegador
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }