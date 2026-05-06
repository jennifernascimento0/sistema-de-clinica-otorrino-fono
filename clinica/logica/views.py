from django.shortcuts import render
from .models import Paciente, Consulta, Profissional

def paciente_list(request):
    # aqui faz a busca de todos os pacientes cadastrados no banco de dados
    pacientes = Paciente.objects.all()
    # e aqui envia os dados para o template paciente_list.html
    return render(request, 'logica/paciente_list.html', {'pacientes': pacientes})

def home(request):
    return render(request, 'logica/home.html')

def consulta_list(request):
    consultas = Consulta.objects.all()
    return render(request, 'logica/consulta_list.html', {'consultas': consultas})

def profissional_list(request):
    profissionais = Profissional.objects.all()
    return render(request, 'logica/profissional_list.html', {'profissionais': profissionais})