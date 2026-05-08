from django import forms
from .models import Profissional, Consulta, Paciente, RegistroConsulta

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

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'telefone', 'email']

class RegistroConsultaForm(forms.ModelForm):
    class Meta:
        model = RegistroConsulta
        fields = ['anamnese', 'avaliacao_vocal', 'diagnostico', 'conduta', 'observacoes']
        widgets = {
            'anamnese': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'avaliacao_vocal': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'conduta': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anamnese'].label = "1. Anamnese"
        self.fields['avaliacao_vocal'].label = "2. Avaliação vocal"
        self.fields['diagnostico'].label = "3. Diagnóstico"
        self.fields['conduta'].label = "4. Conduta"
        self.fields['observacoes'].label = "5. Observações adicionais"