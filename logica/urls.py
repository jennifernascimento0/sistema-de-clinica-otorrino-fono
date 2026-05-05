from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path("admin/", admin.site.urls),
    # pág inicial!!!
    path('', views.home, name='home'),
    # quando o usuário digitar /pacientes/, ele chama a view que a gente criou
    path('pacientes/', views.paciente_list, name='paciente_list'),
]