from django.db import models

class Paciente (models.Model):
    
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Profissional (models.Model):
    ESPECIALIDADE_CHOICES = [
        ('Otorrinolaringologista', 'Otorrinolaringologista'),
        ('Fonoaudiólogo', 'Fonoaudiólogo'),
    ]
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100, 
        choices=ESPECIALIDADE_CHOICES, 
        default='Fonoaudiólogo'
    )
    registro = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional,on_delete=models.CASCADE)
    data = models.DateTimeField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente} - {self.data}"

class RegistroConsulta(models.Model):
    #se o paciente for deletado, os registros somem tbm
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='registros')
    data_atendimento = models.DateTimeField(auto_now_add=True) # aqui salva a data e hora sozinho
    anamnese = models.TextField()
    conduta = models.TextField()
    observacoes = models.TextField(blank=True, null=True)
    diagnostico = models.TextField()
    avaliacao_vocal = models.TextField()

    def __str__(self):
        return f"Atendimento {self.paciente.nome} - {self.data_atendimento.strftime('%d/%m/%Y')}"

    