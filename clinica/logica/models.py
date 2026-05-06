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

    def __str__(self):
        return self.nome
    
class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional,on_delete=models.CASCADE)
    data = models.DateTimeField()
    observacoes = models.TextField()

    def __str__(self):
        return f"{self.paciente} - {self.data}"


    