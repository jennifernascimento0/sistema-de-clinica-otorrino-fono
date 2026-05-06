from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   # path("admin/", admin.site.urls),
    # p�g inicial!!!
    path('', views.home, name='home'),
    #pacientes
    # quando o usu�rio digitar /pacientes/, ele chama a view que a gente criou
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/novo/',views.criar_paciente, name='criar_paciente'),
    path('pacientes/editar/<int:id>/',views.editar_paciente, name='editar_paciente'),
    path('pacientes/deletar/<int:id>/', views.deletar_paciente, name='deletar_paciente'),
    path('consultas/', views.consulta_list,name='consulta_list'),
    path('profissionais/', views.profissional_list, name='profissional_list'),
]