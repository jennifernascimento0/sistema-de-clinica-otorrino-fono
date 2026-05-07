from django.shortcuts import render,redirect, get_object_or_404
from .models import Paciente, Consulta, Profissional
from .forms import ProfissionalForm, ConsultaForm, PacienteForm

#listar parcientes
def paciente_list(request):
    # aqui faz a busca de todos os pacientes cadastrados no banco de dados
    pacientes = Paciente.objects.all()
    # e aqui envia os dados para o template paciente_list.html
    return render(request, 'logica/paciente_list.html', {'pacientes': pacientes})
#criar pacientes
def criar_paciente(request):
    if request.method == 'POST':
        #Paciente.objects.create( 
         #   nome=request.POST .get('nome'),
          #  cpf=request.POST.get('cpf'),
           # telefone=request.POST.get('telefone'),
            #email=request.POST.get('email'))
        #return redirect('paciente_list')
    #return render(request,'pacientes/criar.html')
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paciente_list')
    else:
        form = PacienteForm()
    
    return render(request, 'logica/paciente_form.html', {'form': form})

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
    

def home(request):
    return render(request, 'logica/home.html')

#Consultas

def consulta_list(request):
    consultas = Consulta.objects.all().order_by('data')
    return render(request, 'logica/consulta_list.html', {'consultas': consultas})

#criar consultas
def criar_consulta(request):
    if request.method == 'POST':
        #paciente_id = request.POST .get('paciente')
        #profissional_id = request.POST .get('profissional')

        #paciente = get_object_or_404(Paciente, id=paciente_id)
        #profissional = get_object_or_404(Profissional, id=profissional_id)

        #Consulta.objects.create(
         #   paciente=paciente,
          #  profissional=profissional,
           # data=request.POST.get('data'),
            #observacoes=request.POST.get('observacoes')
        #)
        #return redirect('consulta_list')
    
    #pacientes = Paciente.objects.all()
    #profissionais = Profissional.objects.all()

        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm()
    
    #return render(request, 'consultas/criar.html', {
     #   'pacientes': pacientes,
      #  'profissionais': profissionais
    #})
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



        

#profissional
def profissional_list(request):
    profissionais = Profissional.objects.all()
    return render(request, 'logica/profissional_list.html', {'profissionais': profissionais})

#criar profissionais
def criar_profissional(request):
    if request.method == 'POST':
       # Profissional.objects.create( 
        #    nome=request.POST .get('nome'),
         #   especialidade=request.POST.get('especialidade'),
          #  registro=request.POST.get('registro'))
       # return redirect('profissional_list')

        form = ProfissionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profissional_list')
    else:
        form = ProfissionalForm()
    return render(request,'logica/profissional_form.html', {'form': form})

#editar profissional
def editar_profissional(request,id):
    #busca o paciente pelo id ou retorna erro 404 se n existir
    profissional = get_object_or_404(Profissional, id=id)

    if request.method == 'POST':
        #atuaiza os atributos do objeto
        profissional.nome = request.POST .get('nome')
        profissional.especialidade = request.POST .get('especialidade')
        profissional.registro = request.POST .get('registro')

        profissional.save()
        return redirect('profissional_list')
    return render(request, 'profissionais/editar.html', {'profissional':profissional})

#deletar profissional
def deletar_profissional(request,id):
    profissional = get_object_or_404(Profissional, id=id)

    if request.method == 'POST':
        profissional.delete()
        return redirect('profissional_list')
    