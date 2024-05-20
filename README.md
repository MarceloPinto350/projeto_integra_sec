# Configuração dos ambientes

O ambiente da relização da prova de conceito da solução é composto de:

1. Containetnet - para suportar as configurações das ferramentas de análise de segurança
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
containernet> d1 ifconfig to see config of container d1
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



## Instalação do container com o banco de dados da aplicação AppSeg

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

