import requests
from django.shortcuts import render,redirect, get_object_or_404
from .models import Paciente, Consulta, Profissional, RegistroConsulta
from .forms import ProfissionalForm, ConsultaForm, PacienteForm, RegistroConsultaForm
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
import re
import os

def e_admin(user):
    return user.is_superuser

#listar parcientes
@login_required
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
@login_required
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
@login_required
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
@login_required
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
        
    
@login_required
def home(request):
    return render(request, 'logica/home.html')

#prontuario do paciente
@login_required
def prontuario_paciente(request, id):
    # busca o paciente ou dá erro 404 se n existir
    paciente = get_object_or_404(Paciente, id=id)
    
    # busca todos os registros clínicos desse paciente específico
    historico = RegistroConsulta.objects.filter(paciente=paciente).order_by('-id')

    return render(request, 'logica/prontuario.html', {
        'paciente': paciente, 'historico': historico
    })

#Consultas
@login_required
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


#FUNÇÃO QUE ENVIA O EVENTO (PUB/SUB)
def enviar_evento_consulta(paciente_nome, data_hora):
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    mensagem = f"🔔 **Nova Consulta Agendada!**\n\n👤 Paciente: {paciente_nome}\n📅 Data/Hora: {data_hora}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload, timeout=3)
    except requests.exceptions.RequestException:
        pass  #garante que o Django não trave se o Telegram falhar


#criar consultas
@login_required
def criar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            
            try:
                paciente_nome = str(consulta.paciente)
                data_hora = consulta.data.strftime('%d/%m/%Y %H:%M')
                
                enviar_evento_consulta(paciente_nome, data_hora)
                
            except Exception:
                pass #garante que se houver erro de digitação nos campos, a consulta ainda salva
            
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    return render(request, 'logica/consulta_form.html', {'form': form})
    

@login_required
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

@login_required
def deletar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    consulta.delete()
    return redirect('consulta_list')

@login_required
def registrar_atendimento(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = RegistroConsultaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.paciente = paciente #vincula o atendimento ao paciente da url
            
            try:
                registro.profissional = request.user.perfil_profissional
            except AttributeError:
                # Se o 'admin' puro tentar registrar, ele não tem perfil clínico. 
                # Tratamos isso exibindo um aviso na tela para não quebrar o código.
                messages.error(request, "Apenas usuários com perfil de Profissional de Saúde podem registrar atendimentos.")
                return redirect('prontuario_paciente', id=paciente.id)
            
            registro.save()
            return redirect('prontuario_paciente', id=paciente.id)
    else:
        form = RegistroConsultaForm()
    
    return render(request, 'logica/registro_consulta.html', {
        'form': form, 'paciente': paciente, 'titulo': 'Registrar'
    })

#EDITAR um atendimento existente
@login_required
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
@login_required
def excluir_atendimento(request, id):
    registro = get_object_or_404(RegistroConsulta, id=id)
    paciente_id = registro.paciente.id
    registro.delete()
    #depois de apagar, volta pro prontuário
    return redirect('prontuario_paciente', id=paciente_id)
        

@login_required
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
@login_required
def profissional_list(request):
    termo_busca = request.GET.get('busca')

    if termo_busca:
        # icontains ignora maiúsculas/minúsculas
        profissionais = Profissional.objects.filter(Q(nome__icontains=termo_busca)  | Q(especialidade__icontains=termo_busca))
    else:
        profissionais = Profissional.objects.all()
    
    return render(request, 'logica/profissional_list.html', {'profissionais': profissionais})

#criar profissionais
@login_required
@user_passes_test(e_admin)
def criar_profissional(request):
    if request.method == 'POST':

        form = ProfissionalForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            novo_usuario = User.objects.create_user(
                username=dados['username'],
                password=dados['password'],
                first_name=dados['nome'].split()[0] #pega o primeiro nome para o "Olá, Fulano"
            )
            
            #vincula ao usuário que acabamos de criar
            profissional = form.save(commit=False)
            profissional.user = novo_usuario
            profissional.save()
            
            messages.success(request, f"Profissional {profissional.nome} e login de acesso criados com sucesso!")
            return redirect('profissional_list')
    else:
        form = ProfissionalForm()
    return render(request,'logica/profissional_form.html', {'form': form, 'titulo': 'Cadastrar Novo'})

#editar profissional
@login_required
@user_passes_test(e_admin)
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
@login_required
@user_passes_test(e_admin)
def deletar_profissional(request,id):
    profissional = get_object_or_404(Profissional, id=id)

    if request.method == 'POST':
        profissional.delete()
        return redirect('profissional_list')
    
