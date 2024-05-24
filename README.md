# Configuração do ambiente

O ambiente para realização da prova de conceito para a solução de segurança de software é composto dos seguintes componentes:

1. Containetnet - para suportar as configurações das ferramentas de análise de segurança
   
   1.1. sonar -  servidor da ferramenta Sonar Qube, para análise estática do código fonte das aplicações (SAST)
   
   1.2. sonar_cli - é a máquina responsável pela intercomunicação da Aplicação de Análise de Segurança e o Sonar Qube, via linha de comando
   
   1.3. owasp_zap - servidor da ferramenta OWASP-ZAP, para análise dinâmica das apliações (DAST)

   1.4. owasp_dc - servidor da ferramenta OWASP Dependency Check, para análise de dependência de bibliotecas de terceiros (SCA)


2. Aplicação e banco de dados postgres - para disponibilização da API para integração dos resultados e controle de chamadas às ferramentas de análise de segurança




## Instalação do Containernet:

1. Criar uma VM Ubuntu 22.04 server, limpa, com os pacotes mínimos

   Usuário: cnet
   Senha: cnet

2. Executar os comandos abaixo para proceder a instalação e os testes do containernet em bare metal:
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
containernet> d1 ifconfig 
```

3. Clonar a imagem da aplicação DAMN VULNERABLE WEB APPLICATION (DVWA) que será usada para testes. 

```shell
# 
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



## Configuração do ambiente das aplicações


SonarQube

1. Instalar o SonarQube e Sonar_CLI
2. Acessar usando ambiente através a url<IPserver>:9000
3. Informar usuário e senha: admin/admin
4. indicar nova senha @dm1n e confirmar
5. Clicar em adicionar manualmente o projeto
   5.1. Indique o no do projeto
   5.2. Indique a chave única para o projeto no sonarqube
   5.3 Indique o nome da branch principal do projeto
   5.4 Clique no botão Set Up
6. Concastr nas APIs:
api/authentication/login (POST)
Parâmetros:
   login 
   password
api/authentication/logout (POST)
api/hostspots/search (GET)
   pode ser passado vários paâmetros, mas opcionais
api/hotspots/show
Parâmero:
   hostspot
api/issues/<varias opções>
api/projetc_analyses/<varias opções>
api/user_tokens


Serão clonadas as 


Executar o comando para criação da imagem:
```shell
$ docker run -d --name pg_appseg -e POSTGRES_DB=appseg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v postgres_data:/var/lib/postgresql/data
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

