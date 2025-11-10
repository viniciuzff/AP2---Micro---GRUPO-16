# 🎓 Projeto AP2

INTEGRANTES

- VINICIUS FERREIRA DE FREITAS  RA 2403865

- MURILO LUIZ INÁCIO DE SOUZA RA 2400933
  
- TÚLIO DA SILVA COSTA RA 2302336



## 🧩 Descrição Geral

Este projeto tem como objetivo a construção de **microsserviços em Flask** que permitem o **gerenciamento de professores, turmas, alunos, reservas de sala e atividades/notas**, aplicando uma arquitetura modular e distribuída.

O sistema é dividido em **três microsserviços independentes**, cada um com sua responsabilidade, banco de dados e container próprio, seguindo o padrão **MVC (Model-View-Controller)** e utilizando **SQLAlchemy** para persistência.

---

## 🧠 Arquitetura e Integração entre os Microsserviços

A arquitetura segue o conceito de **microsserviços isolados**, onde cada serviço é independente, mas capaz de se comunicar de forma **síncrona** via **requisições HTTP (REST)**, utilizando a biblioteca `requests`.

Cada serviço expõe sua própria API REST, e as integrações ocorrem através de chamadas entre endpoints:

- O **serviço de Gerenciamento** é responsável pelo **cadastro de alunos, professores e turmas**.  
  Ele fornece **IDs** que são utilizados pelos demais serviços.
  
- O **serviço de Reservas** utiliza o **ID da Turma** para vincular uma **reserva de sala**.  
  Ele **não gerencia turmas diretamente**, apenas consome o ID disponibilizado pelo Gerenciamento.

- O **serviço de Atividades** gerencia **atividades e notas**, utilizando o **ID do Professor** e o **ID da Turma**.  
  Assim como o serviço de Reservas, ele **não gerencia professores ou turmas**, apenas consome seus identificadores.

Essa comunicação síncrona garante integração e consistência entre os microsserviços, sem criar dependências diretas entre os bancos de dados.

## 🧾 Descrição das APIs

- Cada microsserviço possui endpoints REST documentados via Swagger, disponíveis em /apidocs.
- A seguir, os principais endpoints de cada serviço:

## 🟦 Microsserviço de Gerenciamento

- Responsável por alunos, professores e turmas

GET /alunos → Lista todos os alunos

POST /alunos → Cadastra um novo aluno

PUT /alunos/<id> → Atualiza dados de um aluno

DELETE /alunos/<id> → Remove um aluno

GET /professores → Lista professores

POST /professores → Cadastra professor

GET /turmas → Lista turmas

POST /turmas → Cadastra nova turma

## 🟩 Microsserviço de Reservas

Responsável pelas reservas de salas vinculadas às turmas

GET /reservas → Lista todas as reservas

POST /reservas → Cria uma nova reserva (necessário informar id_turma)

GET /reservas/<id> → Detalha uma reserva

DELETE /reservas/<id> → Exclui uma reserva

Integração: este serviço consome o ID da Turma fornecido pelo serviço de Gerenciamento.

## 🟨 Microsserviço de Atividades

- Responsável pelas atividades e notas dos alunos

GET /atividades → Lista todas as atividades

POST /atividades → Cria uma nova atividade (necessário id_professor e id_turma)

PUT /atividades/<id> → Atualiza dados de uma atividade

DELETE /atividades/<id> → Remove uma atividade

## 🧱 Tecnologias Utilizadas

Python 3

Flask – Criação das APIs REST

Flask-SQLAlchemy – ORM para persistência dos dados

SQLite – Banco de dados leve e independente para cada serviço

Flask-Swagger / flasgger – Documentação interativa da API

Docker e Docker Compose – Containerização e orquestração

Requests – Comunicação entre microsserviços

## 📚 Conclusão

O projeto implementa uma arquitetura completa de microsserviços em Flask, com três APIs independentes e comunicação síncrona via requests.
Cada módulo possui seu próprio banco, documentação Swagger e rotas REST, oferecendo uma base sólida para aplicações distribuídas.
