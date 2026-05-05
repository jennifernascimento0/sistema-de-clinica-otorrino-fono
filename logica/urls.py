from django.urls import path
from . import views

urlpatterns = [
    # quando o usuário digitar /pacientes/, ele chama a view que a gente criou
    path('pacientes/', views.paciente_list, name='paciente_list'),
]