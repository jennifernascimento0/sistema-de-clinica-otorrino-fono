from django.shortcuts import render,redirect, get_object_or_404
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

#editar pacientes
def editar_paciente(request,id):
    #busca o paciente pelo id ou retorna erro 404 se n existir
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        #atuaiza os atributos do objeto
        paciente.nome = request.POST .get('nome')
        paciente.cpf = request.POST .get('cpf')
        paciente.telefone = request.POST .get('telefone')
        paciente.email = request.POST .get('email')

        paciente.save()
        return redirect('paciente_list')
    return render(request, 'pacientes/editar.html', {'paciente':paciente})

#deletar paciente
def deletar_paciente(request,id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.delete()
        return redirect('paciente_list')
    #a gnt pode colocar uma tela de confirmação caso acesse via get
    return render(request, 'pacientes/confirmar_delecao.html', {'paciente':paciente})

def home(request):
    return render(request, 'logica/home.html')

def consulta_list(request):
    consultas = Consulta.objects.all()
    return render(request, 'logica/consulta_list.html', {'consultas': consultas})
#profissional
def profissional_list(request):
    profissionais = Profissional.objects.all()
    return render(request, 'logica/profissional_list.html', {'profissionais': profissionais})

#criar profissionais
def criar_profissional(request):
    if request.method == 'POST':
        Profissional.objects.create( 
            nome=request.POST .get('nome'),
            especialidade=request.POST.get('especialidade'),
            registro=request.POST.get('registro'))
        return redirect('profissional_list')
    return render(request,'profissional/criar.html')