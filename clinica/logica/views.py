import requests
from django.shortcuts import render,redirect, get_object_or_404
from .models import Paciente, Consulta, Profissional, RegistroConsulta
from .forms import ProfissionalForm, ConsultaForm, PacienteForm, RegistroConsultaForm
from django.db.models import Q
from django.views.decorators.cache import cache_page
import re

#listar parcientes
@cache_page(60)
def paciente_list(request):
    termo_busca = request.GET.get('busca')

    if termo_busca:
        #apenas_numeros = re.sub(r'\D', '', termo_busca)
        # icontains ignora maiúsculas/minúsculas
        pacientes = Paciente.objects.filter(
            Q(nome__icontains=termo_busca) | 
            Q(cpf__icontains=termo_busca) #|
           # Q(cpf__icontains=apenas_numeros)
            )
    else:
        pacientes = Paciente.objects.all()
    
    return render(request, 'logica/paciente_list.html', {'pacientes': pacientes})

#criar pacientes
def criar_paciente(request):
    if request.method == 'POST':

        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm()
    
    return render(request, 'logica/paciente_form.html', {'form': form, 'titulo': 'Cadastrar'})

#editar pacientes
def editar_paciente(request,id):
    #busca o paciente pelo id ou retorna erro 404 se n existir
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        #atuaiza os atributos do objeto
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm(instance=paciente) # esse instance preenche automaticamente
    
    return render(request, 'logica/paciente_form.html', {'form': form, 'titulo': 'Editar'})

#deletar paciente
def deletar_paciente(request,id):
    paciente = get_object_or_404(Paciente, id=id)

    requests.post(
        'http://127.0.0.1:5000/excluir',
        json={
            'id':paciente.id,
            'nome':paciente.nome,
            'cpf':paciente.cpf,
            'telefone':paciente.telefone,
            'email':paciente.email
        }
    )
    paciente.delete()
    return redirect('paciente_list')
        
    

def home(request):
    return render(request, 'logica/home.html')

#prontuario do paciente
def prontuario_paciente(request, id):
    # busca o paciente ou dá erro 404 se n existir
    paciente = get_object_or_404(Paciente, id=id)
    
    # busca todos os registros clínicos desse paciente específico
    historico = RegistroConsulta.objects.filter(paciente=paciente).order_by('-id')

    return render(request, 'logica/prontuario.html', {
        'paciente': paciente, 'historico': historico
    })

#Consultas

def consulta_list(request):
    termo_busca = request.GET.get('busca')
    
    if termo_busca:
        #busca pelo nome do paciente ou nome do profissional
        consultas = Consulta.objects.filter(
            paciente__nome__icontains=termo_busca
        ) | Consulta.objects.filter(
            profissional__nome__icontains=termo_busca
        )
    else:
        consultas = Consulta.objects.all().order_by('data')
    return render(request, 'logica/consulta_list.html', {'consultas': consultas})

#criar consultas
def criar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    return render(request, 'logica/consulta_form.html', {'form': form})

def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == 'POST':
        consulta.paciente = get_object_or_404(Paciente, id=request.POST.get('paciente'))
        consulta.profissional = get_object_or_404(Profissional, id=request.POST.get('profissional'))
        consulta.data = request.POST.get('data')
        consulta.observacoes = request.POST.get('observacoes')
        consulta.save()
        return redirect('consulta_list')

    return render(request, 'consultas/editar.html', {
        'consulta': consulta,
        'pacientes': Paciente.objects.all(),
        'profissionais': Profissional.objects.all()
    })

def deletar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    consulta.delete()
    return redirect('consulta_list')

def registrar_atendimento(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = RegistroConsultaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.paciente = paciente #vincula o atendimento ao paciente da url
            registro.save()
            return redirect('prontuario_paciente', id=paciente.id)
    else:
        form = RegistroConsultaForm()
    
    return render(request, 'logica/registro_consulta.html', {
        'form': form, 'paciente': paciente, 'titulo': 'Registrar'
    })

#EDITAR um atendimento existente
def editar_atendimento(request, id):
    registro = get_object_or_404(RegistroConsulta, id=id)
    #instance=registro faz o form ficar já preenchido!!!! n esquecer de colocar em tudo que for editar
    if request.method == 'POST':
        form = RegistroConsultaForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            #depois de editar, volta pro prontuário do paciente
            return redirect('prontuario_paciente', id=registro.paciente.id)
    else:
        form = RegistroConsultaForm(instance=registro)
    
    return render(request, 'logica/registro_consulta.html', {
        'form': form,
        'paciente': registro.paciente, 'titulo': 'Editar'
    })

#EXCLUIR um atendimento
def excluir_atendimento(request, id):
    registro = get_object_or_404(RegistroConsulta, id=id)
    paciente_id = registro.paciente.id
    registro.delete()
    #depois de apagar, volta pro prontuário
    return redirect('prontuario_paciente', id=paciente_id)
        

def agenda_calendario(request):
    termo_busca = request.GET.get('busca')
    if termo_busca:
        consultas = Consulta.objects.filter(
            Q(paciente__nome__icontains=termo_busca) | 
            Q(profissional__nome__icontains=termo_busca) |
            Q(profissional__especialidade__icontains=termo_busca)
        ).distinct() # distinct evita duplicatas se o termo bater em mais de um campo
    else:
        consultas = Consulta.objects.all()

    return render(request, 'logica/agenda_calendario.html', {'consultas': consultas})


#profissional
def profissional_list(request):
    termo_busca = request.GET.get('busca')

    if termo_busca:
        # icontains ignora maiúsculas/minúsculas
        profissionais = Profissional.objects.filter(Q(nome__icontains=termo_busca)  | Q(especialidade__icontains=termo_busca))
    else:
        profissionais = Profissional.objects.all()
    
    return render(request, 'logica/profissional_list.html', {'profissionais': profissionais})

#criar profissionais
def criar_profissional(request):
    if request.method == 'POST':

        form = ProfissionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profissional_list')
    else:
        form = ProfissionalForm()
    return render(request,'logica/profissional_form.html', {'form': form, 'titulo': 'Cadastrar Novo'})

#editar profissional
def editar_profissional(request,id):
    #busca o paciente pelo id ou retorna erro 404 se n existir
    profissional = get_object_or_404(Profissional, id=id)

    if request.method == 'POST':
    # instance=profissional pra os dados sejam salvos no profissional certo
        form = ProfissionalForm(request.POST, instance=profissional)
        if form.is_valid():
            form.save()
            return redirect('profissional_list')
    else:
        form = ProfissionalForm(instance=profissional)
    
    return render(request, 'logica/profissional_form.html', {
        'form': form, 'titulo': 'Editar'
    })

#deletar profissional
def deletar_profissional(request,id):
    profissional = get_object_or_404(Profissional, id=id)

    if request.method == 'POST':
        profissional.delete()
        return redirect('profissional_list')
    
