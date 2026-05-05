from django.contrib import admin
from .models import Paciente, Profissional, Consulta

admin.site.register(Paciente)
admin.site.register(Profissional)
admin.site.register(Consulta)