from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   # path("admin/", admin.site.urls),
    #pag inicial
    path('', views.home, name='home'),
    #pacientes
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/novo/',views.criar_paciente, name='criar_paciente'),
    path('pacientes/editar/<int:id>/',views.editar_paciente, name='editar_paciente'),
    path('pacientes/deletar/<int:id>/', views.deletar_paciente, name='deletar_paciente'),
    path('pacientes/prontuario/<int:id>/', views.prontuario_paciente, name='prontuario_paciente'),
    path('pacientes/atendimento/<int:paciente_id>/', views.registrar_atendimento, name='registrar_anamnese'),
    path('atendimento/editar/<int:id>/', views.editar_atendimento, name='editar_atendimento'),
    path('atendimento/excluir/<int:id>/', views.excluir_atendimento, name='excluir_atendimento'),

    #consultas
    path('consultas/', views.consulta_list,name='consulta_list'),
    path('consultas/novo/', views.criar_consulta, name='criar_consulta'),
    path('consultas/editar/<int:id>/', views.editar_consulta, name='editar_consulta'),
    path('consultas/deletar/<int:id>/', views.deletar_consulta, name='deletar_consulta'),


    #profissionais
    path('profissionais/', views.profissional_list, name='profissional_list'),
    path('profissionais/novo/', views.criar_profissional, name='criar_profissional'),
    path('profissionais/editar/<int:id>/', views.editar_profissional, name='editar_profissional'),
    path('profissionais/deletar/<int:id>/', views.deletar_profissional, name='deletar_profissional'),
]