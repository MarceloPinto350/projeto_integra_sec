# Proposta do Sistema de gerenciamento de segurança de aplicações - Apoio ao DevSecOps


## Resumo:

O presente trabalho apresenta uma ferramenta integrada para validação de segurança de software, abrangendo as abordagens SAST (Static Application Security Testing), SCA (Software Composition Analysis), DAST (Dynamic Application Security Testing) e integração dos resultados de forma centralizada. A ferramenta atua em um framework composto pelas ferramentas SonarQube (SAST), Owasp Dependency Check (SCA), Owasp ZAP (DAST),  Gitlab ou Github (repositórios de código fonte) e uma aplicação desenvolvida em Python + Django + Javascript + banco de dados Postgresql, visando possibilitar cadastrar as aplicações, suas configurações referentes à varreduras de segurança, manter a API para execução das varreduras e possibilitar a consulta das aplicações, seus relacionamentos com as ferramentas de segurança e os dados históricos dos resultados das varreduras realizadas, conforme os resultados obtidos a partir dos  processos de varredura de segurança realizados e armazenados no  banco de dados.


## Introdução:

A segurança de software é um aspecto crucial no desenvolvimento de aplicações web, especialmente em cenários que lidam com dados sensíveis. Os estudos demonstram que a complexidade das aplicações e a proliferação de vulnerabilidades exigem abordagens abrangentes e automatizadas para garantir a segurança e confiabilidade do software, entretanto grande parte dos relatos retratam a automação através de pipelines CI/CD usando Gitlab ou Github, de forma que as informações relativas aos resultados das varreduras ficam armazenados nas ferramentas, dificultando o monitoramento por parte dos desenvolvedores e especialistas em segurança que precisam conhecer as diversas ferramentas para operá-las e colher os resultados de forma mais eficiente.


## Ferramenta Integrada para Validação de Segurança:

A ferramenta proposta neste trabalho visa a integração de diversas ferramentas de segurança de software, com base em um framework básico preliminar com uso de ferramentas líderes em seus respectivos domínios, conforme estudo realizado:

   **SonarQube**: Ferramenta SAST que identifica vulnerabilidades de código estático, problemas de qualidade de código e potenciais violações de segurança.

   Snyk: Ferramenta SCA que analisa as dependências de software para detectar vulnerabilidades conhecidas e componentes obsoletos.
   
   **Owasp Dependency Check**: Ferramenta SCA que complementa o Snyk, fornecendo análises de segurança adicionais para dependências de software.
   
   **Owasp ZAP**: Ferramenta DAST que realiza testes dinâmicos de segurança, detectando vulnerabilidades durante a execução da aplicação.

   **Gitlab ou Github**: Plataformas de gerenciamento de código-fonte que facilitam a integração e automação dos processos de varredura de segurança.

   **Aplicação Python com Django, Javascript e banco de dados Postgresql**: Aplicação web que centraliza as informações das aplicações a serem  analisadas e realiza a execução das varreduras de segurança, armazenando os resultados e possibilita a consulta dos resultados, fornecendo uma interface amigável para gerenciamento e visualização dos dados.


## Integração e expansão da solução:

A proposta consiste na criação de uma API REST em Python para automatizar o processo de validação de segurança em aplicações web.A API receberá informações sobre a aplicação a ser varrida e obterá, da base de dados da aplicação, as demais informações necessárias para a execução das varreduras de segurança às quais estiver vinculada. A API processará a chamada ferramenta adequada para cada caso e os resultados das varreduras serão armazenados em formato JSON em um banco de dados Postgres associado à API.

A ferramenta fornecerá uma interface amigável para gerenciamento das aplicações e visualização dos resultados, permitindo aos desenvolvedores e equipes de segurança acompanhar o status da segurança da aplicação e tomar medidas necessárias para correção, antes da liberação da aplicação para ambientes de produção.


## Funcionalidades da aplicação e API:

*  Cadastro de Aplicações: A aplicação permitirá o cadastro de novas aplicações web, incluindo informações como nome, URL e URL do código-fonte armazenado no GitLab ou GitHub, tipos de varredura que a mesma está sujeita

*  Execução de Varreduras de Segurança: A API fornecerá endpoints para acionar a execução das varreduras de segurança SAST, DAST e SCA para as aplicações cadastradas, conforme o caso.

*  Armazenamento de Resultados: Os resultados das varreduras de segurança serão armazenados em formato JSON em um banco de dados Postgres.

* Consulta de Resultados: A aplicação fornecerá consulta das aplicações e dos resultados das varreduras de segurança armazenados no banco de dados, em formato de Grafos.


## Benefícios do uso de ferramenta integrada:

A adoção de API possibilita a automação da validação de segurança, viabilizando a chamada da varredura através do pipeline CI/CD ou diretamente na aplicação. Além disso, 	possibilita a integração com ferramentas de terceiros e pode ser facilmente escalonada para atender às necessidades de inclusão de varreduras através de outras ferramentas, conforme a expansão do uso da solução, reduzindo o tempo e o esforço necessários para identificar e corrigir vulnerabilidades.

Além disso, outro ponto relevante a ser destacado diz respeito à centralização de resultados em um único local, facilitando a consulta, análise dos dados e maior transparências às equipes de TI envolvidas no cliclo de vida do software da organização.


## Implementação da aplicação:

A implementação da aplicação envolve as seguintes etapas:

* Criação do projeto Django

* Definição dos modelos de dados para aplicações e resultados de varreduras

* Configuração do banco de dados Postgres

* Implementação dos cadastros de aplicações e demais cadastros básicos

* Implementação dos acionamentos de varreduras de segurança

* Desenvolvimento da API REST

* Integração com as ferramentas de análise de segurança

* Implementação da lógica para acionamento das varreduras de segurança SAST, DAST e SCA

* Tratamento dos resultados das varreduras de segurança e conversão para o formato JSON

* Armazenamento de Resultados

* Implementação da consulta das aplicações e resultados das pesquisas


## Considerações Adicionais para futura implementação:

1. A aplicação deverá ser protegida por autenticação e autorização para controlar o acesso aos seus recursos
2. A aplicação poderá ser integrada com ferramentas de monitoramento e notificação para alertar os usuários sobre a presença de  vulnerabilidades críticas
3. A API poderá ser estendida para incluir suporte a outras ferramentas de segurança de software e funcionalidades adicionais.


## Benefícios esperados com uso da ferramenta integrada:

A ferramenta proposta oferece diversos benefícios, incluindo:

Abordagem Abrangente: Abrange as principais abordagens de validação de segurança de software (SAST, SCA e DAST), fornecendo uma visão completa da segurança da aplicação.

Automação: Automatiza os processos de varredura de segurança, reduzindo o tempo e o esforço necessários para identificar e corrigir vulnerabilidades.

Centralização de Resultados: Armazena e centraliza os resultados das varreduras em um único local, facilitando a consulta e análise dos dados.

Interface Amigável: Fornece uma interface amigável para gerenciamento e visualização dos resultados, permitindo aos usuários acompanhar o status da segurança da aplicação.


## Conclusão:

A ferramenta integrada proposta neste trabalho oferece uma solução que pode ser abrangente e automatizada para validação de segurança de software em aplicações web, aliada à centralização de resultados e à interface amigável, torna a ferramenta um recurso valioso para desenvolvedores e equipes de segurança que buscam garantir a segurança e confiabilidade de suas aplicações e de maneira mais genérica como forte apoio à adoção da cultura DevSecOps na organização.


**Palavras-chave**: SAST, SCA, DAST, SonarQube, Owasp Dependency Check, Owasp ZAP, Gitlab, Django, Javascript, Postgres, Integração,





# Configuração dos ambientes

O ambiente da relização da prova de conceito da solução é composto de:

1. Containetnet - para suportar as configurações das ferramentas de análise de segurança
2. Aplicação e banco de dados postgres - para disponibilização da API para integração dos resultados e controle de chamadas às ferramentas de análise de segurança



## Instalação do Containernet:

1. Criar uma VM Ubuntu 22.04 server, limpa, com os pacotes mínimos

   Usuário: cnet

   Senha: cnet

2. Executar os comandos abaixo para instalar e testar a instalçai do containernet em bare metal:
```shell
# Instalar ansible
~$ sudo apt install git ansible -y
# Clonar e instalar o containernet
~$ git clone https://github.com/ramonfontes/containernet.git
~$ cd containernet
~/containernet$ sudo util/install.sh -W

# Executar os comandos abaixo par testar se a instalação do containernet
~/containernet$ cd containernet
~/containernet/containernet$ sudo python examples/containernet_example.py
containernet> d1 ifconfig to see config of container d1
```


## Instalação do container com o banco de dados da aplicação

Executar o comando para criação da imagem:
```shell
$ docker run -d --name pg_appseg -e POSTGRES_DB=appseg -e POSTGRES_USER=postgres -e POSdcTGRES_PASSWORD=postgres -p 5432:5432 -v postgres_data:/var/lib/postgresql/data
```

Clonar o projeto para a pasta local
```shell
git clone ...
```

Executar o comando para fazer a migração das classes para tabelas de banco de dados
```shell
$ python manage.py makemigrations
```

Efetivar a migração e criação das tabelas referentes às classes mapeadas
```shell
$ python manage.py migrate
```

Criar o superusuário para administração da aplicação
```shell
$ python manage.py createsuperuser

#Informar
#Usuário: admin
#e-mail: admin@admin.com
#Senha: admin
```

## Arquitetura do framework de análise

Serão utilizadas na prova de conceito as seguintes ferramentas, conforme o tipo de teste:

* SAST: SonarQube
* SCA: OWASP Dependençy Check
* DAST: OWASP ZAP ** e Burp Suite CE ???**


Serão utilizadas as seguintes aplicações para realização de testes:

**Sistema de biblioteca BIBPUB-IMD**, é uma aplicação web desenvolvida em Python + Django + Postgres, cujo principal objetivo foi servir de case de desenvolvimento web para as disciplinas de Desenvolvimento Web 2 e Testes de Software; Repositório: GitHub -  https://github.com/MarceloPinto350/bibpub.git; Imagem docker: docker push marcelopinto350/bibpub:<tagname>

**Damn Vulnerable Web Application (DVWA)** é uma aplicação web desenvolvida  PHP + MySQL com a finalidade de praticar algumas das mais comuns vulnerabilidades web, com vário níveis de dificuldade; Repositório: Github: https://github.com/digininja/DVWA.git; imagem docker: ...

