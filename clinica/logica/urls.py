from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   # path("admin/", admin.site.urls),
    # p�g inicial!!!
    path('', views.home, name='home'),
    # quando o usu�rio digitar /pacientes/, ele chama a view que a gente criou
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('consultas/', views.consulta_list,name='consulta_list'),
    path('profissionais,', views.profissional_list, name='profissional_list'),
]