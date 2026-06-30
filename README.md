# Sistema de Clínica Otorrino e Fono



## Sobre o projeto

O Sistema de Clínica Otorrino e Fono é uma aplicação web desenvolvida para auxiliar no gerenciamento de uma clínica de Otorrinolaringologia e Fonoaudiologia. O sistema permite o cadastro e gerenciamento de pacientes, profissionais de saúde, consultas e prontuários, centralizando as principais atividades administrativas da clínica.

O projeto foi desenvolvido utilizando a arquitetura MVC (Model-View-Controller) com Django, empregando banco de dados PostgreSQL, cache com Redis, autenticação de usuários, microsserviços e implantação em ambiente de produção na AWS.

Projeto desenvolvido pelas alunas Jennifer de Oliveira e Marcela Helena, do 4º período de Análise e Desenvolvimento de Sistemas (ADS) do IFPE campus Paulista, para a disciplina de Desenvolvimento Web II lecionada pelo prof. Rodrigo Lira, utilizando Django e os principais conceitos de desenvolvimento de aplicações web modernas, incluindo arquitetura MVC, PostgreSQL, Redis, microsserviços, autenticação, CI/CD e implantação em nuvem.



---



## Tecnologias Utilizadas (Requisitos ii, iv, v, viii, ix, x)

* *Backend:* Python 3 / Django 5.2

* *Frontend:* HTML5 / CSS3 / Bootstrap 5

* *Banco de Dados Relacional:* PostgreSQL (Substituindo o SQLite padrão)

* *Estratégia de Cache:* Redis

* *Componente de Microsserviço:* Flask / Requests (Comunicação Síncrona HTTP)

* *Infraestrutura em Nuvem:* AWS EC2 (Ubuntu Server) / Gunicorn

* *Controle de Versão:* Git / GitHub (Histórico completo de evolução)

* *Integração Contínua (CI/CD):* GitHub Actions (.github/workflows/django.yml)



---



## Funcionalidades e Entidades (Requisito i)



### 1. Gerenciamento de Pacientes (Entidade 1)

* Cadastro completo de novos pacientes com validação de campos.

* Listagem dinâmica e edição de informações cadastrais.

* Exclusão de registros integrada ao microsserviço de auditoria.

* Busca inteligente por nome ou CPF.



### 2. Gerenciamento de Profissionais (Entidade 2)

* Cadastro e atualização de profissionais de saúde.

* Vinculação obrigatória de especialidades clínicas (Otorrinolaringologia ou Fonoaudiologia).

* Listagem e busca por nome ou especialidade.



### 3. Gerenciamento de Consultas e Prontuários (Entidade 3)

* Agendamento, alteração e cancelamento de consultas médicas.

* Visualização da agenda integrada.

* Registro de atendimentos clínicos e prontuários históricos associados ao paciente.



---



## Autenticação e Regras de Negócio (Requisitos vi, vii)



### Autenticação de Usuários

* Restrição total de acesso às funcionalidades administrativas do sistema.

* Sistema de login e controle de sessão seguro nativo do Django (auth_user).



### Regras de Negócio Implementadas

* *Pacientes:* Todos os campos obrigatórios do prontuário eletrônico devem ser preenchidos de forma válida.

* *Profissionais:* Todo profissional de saúde deve possuir uma especialidade ativa cadastrada no sistema.

* *Consultas:* Toda consulta deve estar estritamente vinculada a um paciente existente e a um profissional disponível.

* *Prontuários:* Todo registro clínico ou evolução deve estar associado ao histórico de um paciente.



---



## Componentes Avançados de Arquitetura (Requisito iv)



### 1. Microsserviço Independente (Auditoria de Exclusões)

O sistema utiliza um *Microsserviço independente em Flask* responsável exclusivamente pela auditoria e registro das exclusões de pacientes do sistema principal.

* *Fluxo:* O usuário solicita a exclusão no Django, uma requisição HTTP síncrona é enviada ao Flask, o Flask anota os detalhes localmente no arquivo registro.txt, o registro é deletado do PostgreSQL.



### 2. Padrão Publish-Subscribe / Event-Driven (Notificações via Telegram)

Para cumprir a arquitetura baseada em eventos, o sistema implementa uma dinâmica de *Publish-Subscribe*. 

* *Publisher (Django):* Quando uma nova consulta é criada ou alterada no sistema, a aplicação "publica" esse evento disparando uma notificação assíncrona externa.

* *Subscriber (Bot do Telegram):* O bot atua como o consumidor desse evento, recebendo os dados da consulta e encaminhando de forma imediata o alerta de confirmação para os canais configurados.



---



## Estratégia de Cache (Requisito viii)

Para reduzir consultas repetidas ao banco de dados PostgreSQL e otimizar o tempo de resposta do servidor na nuvem, foi implementada a estratégia de cache em rotas de grande acesso:

* *Exemplo aplicado:* Utilização do decorator @cache_page(60) na listagem de pacientes (paciente_list), mantendo os dados em memória por 1 minuto antes de realizar uma nova consulta pesada no banco.



---



## Como Acessar o Projeto em Produção (Requisito v)



### Link de Acesso Direto

A aplicação está implantada e rodando na nuvem da AWS. Você pode acessar o sistema pronto através do link abaixo:

**[Acessar o Sistema da Clínica na AWS EC2](http://ec2-54-81-241-151.compute-1.amazonaws.com:8000/logica/)**



### Comandos para Execução e Logs no Servidor

Caso seja necessário interagir ou verificar os serviços dentro da instância Ubuntu Server da AWS:



1. *Ativar o ambiente virtual e acessar o projeto:*

   cd Sistema-de-clinica-otorrino-fono/clinica
   source venv/bin/activate

2. Comando de inicialização do Microsserviço (Flask):
python microsservico.py &


3. Comando de inicialização do Servidor Django (Gunicorn com timeout de produção):
gunicorn clinica.wsgi:application --bind 0.0.0.0:8000 --timeout 300 --workers 3 &


4. Visualizar o arquivo de logs gerado pelo microsserviço (Auditoria):
cat registro.txt


# Diagrama do projeto

<img width="1080" height="510" alt="image" src="https://github.com/user-attachments/assets/bb2831c0-ea37-4e66-b3fa-937278077aab" />

