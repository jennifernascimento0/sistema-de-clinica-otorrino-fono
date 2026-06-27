from django import forms
from django.contrib.auth.models import User
from .models import Profissional, Consulta, Paciente, RegistroConsulta

class ProfissionalForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        label="Nome de Usuário (Login)", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: rodrigo.lira'})
    )
    password = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'})
    )
    password_confirm = forms.CharField(
        label="Confirme a Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'})
    )
    class Meta:
        model = Profissional
        fields = ['nome', 'especialidade', 'registro', 'telefone'] #tudo o que quiser que apareça
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

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