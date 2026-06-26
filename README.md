# Sistema de Clínica Otorrino e Fono

## Sobre o projeto

O **Sistema de Clínica Otorrino e Fono** é uma aplicação web desenvolvida para auxiliar no gerenciamento de uma clínica de Otorrinolaringologia e Fonoaudiologia. O sistema permite o cadastro e gerenciamento de pacientes, profissionais de saúde, consultas e prontuários, centralizando as principais atividades administrativas da clínica.

O projeto foi desenvolvido utilizando a arquitetura **MVC (Model-View-Controller)** com Django, empregando banco de dados PostgreSQL, cache com Redis, autenticação de usuários, microsserviços e implantação em ambiente de produção na AWS.

---

# Funcionalidades

## Gerenciamento de Pacientes

* Cadastro de pacientes;
* Listagem de pacientes;
* Edição de informações;
* Exclusão de pacientes;
* Busca por nome ou CPF.

## Gerenciamento de Profissionais

* Cadastro de profissionais;
* Listagem de profissionais;
* Atualização de dados;
* Exclusão de profissionais;
* Busca por nome ou especialidade.

## Gerenciamento de Consultas

* Agendamento de consultas;
* Alteração de consultas;
* Cancelamento de consultas;
* Consulta da agenda.

## Gerenciamento de Prontuários

* Registro de atendimentos;
* Atualização de registros clínicos;
* Exclusão de registros;
* Visualização do histórico de atendimentos.

## Autenticação

* Login de usuários;
* Restrição de acesso às funcionalidades do sistema por autenticação.

---

# Arquitetura MVC

O projeto segue a arquitetura **MVC**, promovendo a separação entre dados, regras de negócio e interface.

## Model

Responsável pela representação das entidades do sistema e pelo acesso ao banco de dados.

Principais modelos:

* Paciente
* Profissional
* Consulta
* RegistroConsulta

## View

Responsável pelo processamento das requisições, aplicação das regras de negócio e comunicação entre os modelos e os templates.

Exemplos de views:

* paciente_list
* criar_paciente
* consulta_list
* registrar_atendimento

## Template

Responsável pela interface gráfica apresentada ao usuário.

Tecnologias utilizadas:

* HTML5
* CSS3
* Bootstrap 5

---

# Tecnologias Utilizadas

## Backend

* Python 3
* Django 6

## Frontend

* HTML5
* CSS3
* Bootstrap 5

## Banco de Dados

* PostgreSQL

## Cache

* Redis

## Microsserviço

* Flask
* Requests

## Infraestrutura

* AWS EC2
* Ubuntu Server

## Controle de Versão

* Git
* GitHub

## Integração Contínua

* GitHub Actions

---

# Banco de Dados

O sistema utiliza o PostgreSQL como banco de dados relacional.

Principais entidades:

* Paciente
* Profissional
* Consulta
* RegistroConsulta
* auth_user

---

# Microsserviço

O sistema utiliza um microsserviço independente responsável pelo registro das exclusões de pacientes.

Fluxo de funcionamento:

1. O usuário solicita a exclusão de um paciente.
2. O sistema Django envia uma requisição HTTP para o microsserviço.
3. O microsserviço registra a exclusão.
4. O paciente é removido do banco principal.

Essa abordagem demonstra a comunicação entre aplicações independentes utilizando arquitetura baseada em microsserviços.

---

# Estratégia de Cache

Foi implementado cache utilizando Redis com o objetivo de reduzir consultas repetidas ao banco de dados e melhorar o desempenho da aplicação.

Exemplo de utilização:

```python
@cache_page(300)
def paciente_list(request):
```

As informações permanecem armazenadas em cache por 5 minutos, reduzindo o tempo de resposta para consultas frequentes.

---

# CI/CD

O projeto utiliza GitHub Actions para automatizar parte do processo de integração contínua.

A pipeline realiza:

* Checkout do código;
* Instalação das dependências;
* Execução das migrações;
* Verificação da aplicação Django.

Arquivo de configuração:

```
.github/workflows/django.yml
```

---

# Implantação em Nuvem

A aplicação foi implantada em uma instância AWS EC2 utilizando Ubuntu Server.

Componentes utilizados:

* Amazon EC2
* PostgreSQL
* Redis

Essa infraestrutura permite a execução da aplicação em ambiente de produção, atendendo aos requisitos da disciplina.

---

# Regras de Negócio

## Pacientes

* CPF deve ser único;
* Todos os campos obrigatórios devem ser preenchidos.

## Profissionais

* Todo profissional deve possuir uma especialidade cadastrada.

## Consultas

* Toda consulta deve estar vinculada a um paciente e a um profissional.

## Prontuários

* Todo registro clínico deve estar associado a um paciente.

---

# Estrutura do Projeto

```
clinica/
├── models.py
├── views.py
├── urls.py
├── templates/
├── static/
├── microsservico.py
└── settings.py
```

---

# Desenvolvedores

Projeto desenvolvido pelas alunas Jennifer de Oliveira e Marcela Helena, do 4º período de Análise e Desenvolvimento de Sistemas (ADS) do IFPE campus Paulista, para a disciplina de Desenvolvimento Web II lecionada pelo prof. Rodrigo Lira, utilizando Django e os principais conceitos de desenvolvimento de aplicações web modernas, incluindo arquitetura MVC, PostgreSQL, Redis, microsserviços, autenticação, CI/CD e implantação em nuvem.
