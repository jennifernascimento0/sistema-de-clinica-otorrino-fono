from django.shortcuts import render
from .models import Paciente

def paciente_list(request):
    # aqui faz a busca de todos os pacientes cadastrados no banco de dados
    pacientes = Paciente.objects.all()
    # e aqui envia os dados para o template paciente_list.html
    return render(request, 'logica/paciente_list.html', {'pacientes': pacientes})