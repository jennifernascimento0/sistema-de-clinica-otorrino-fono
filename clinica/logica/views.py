from django.shortcuts import render,redirect
from .models import Paciente, Consulta, Profissional
#listar parcientes
def paciente_list(request):
    # aqui faz a busca de todos os pacientes cadastrados no banco de dados
    pacientes = Paciente.objects.all()
    # e aqui envia os dados para o template paciente_list.html
    return render(request, 'logica/paciente_list.html', {'pacientes': pacientes})
#criar pacientes
def criar_paciente(request):
    if request.method == 'POST':
        Paciente.objects.create( 
            nome=request.POST .get('nome'),
            cpf=request.POST.get('cpf'),
            telefone=request.POST.get('telefone'),
            email=request.POST.get('email'))
        return redirect('paciente_list')
    return render(request,'pacientes/criar.html')

def home(request):
    return render(request, 'logica/home.html')

def consulta_list(request):
    consultas = Consulta.objects.all()
    return render(request, 'logica/consulta_list.html', {'consultas': consultas})

def profissional_list(request):
    profissionais = Profissional.objects.all()
    return render(request, 'logica/profissional_list.html', {'profissionais': profissionais})