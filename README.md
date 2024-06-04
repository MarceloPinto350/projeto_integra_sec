# Configuração do ambiente

O ambiente para realização da prova de conceito para a solução de segurança de software é composto dos seguintes componentes:

1. Containetnet - para suportar as configurações das ferramentas de análise de segurança
   
   1.1. sonar -  servidor da ferramenta Sonar Qube, para análise estática do código fonte das aplicações (SAST)
   
   1.2. sonar_cli - é a máquina responsável pela intercomunicação da Aplicação de Análise de Segurança e o Sonar Qube, via linha de comando
   
   1.3. owasp_zap - servidor da ferramenta OWASP-ZAP, para análise dinâmica das apliações (DAST)

   1.4. owasp_dc - servidor da ferramenta OWASP Dependency Check, para análise de dependência de bibliotecas de terceiros (SCA)


2. Aplicação e banco de dados postgres - para disponibilização da API para integração dos resultados e controle de chamadas às ferramentas de análise de segurança




## Configuração do ambiente


### Criar uma VM Ubuntu 22.04 server
1. Requisitos:
   * A configuração do Ubuntu Server deverá ser com os pacotes mínimos (minimal server) e OpenSSH Server instalado
      * Hostname: containernet (sugestão)
      * Usuário padrão: docker (sugestão)
      * Senha: docker (sugestão)    
   * Memmória: 4Gb
   * Processadores: 4
   * Armazenamento: 25Gb
   * Rede: Placa em modo Bridge

### Instalação do Containernet

Para configuração do Containernet se deve acessar a máquina virtual através de SSH e proceder os seguintes passos para atualização do servidor e instalação do a:

```shell
# Atualizar as configurações da máquina e intalar o Git e o Ansible
~$ sudo apt update && sudo apt upgrade -y && sudo apt install vim nano git ansible -y

# Clonar e instalar o containernet 
~$ git clone https://github.com/ramonfontes/containernet.git

# Proceder a instalação do containernet
~$ cd containernet
~/containernet$ sudo util/install.sh -W
# Confirmar eventuais necessidades de reinicialização de serviços
# ajustado erro no trecho '-u', '0, '%s... (sem fechamento das aspas no 0)
# Ajustar configuração do containernet, para integração do ambiente, conforme indicado:
# alterar linha containernet/node.py#L304 para:
# cmd = ['docker', 'exec', '-it', '-u', '0', '%s' % self.did, 'env', 'PS1=' + chr(127),
#alterar linha containernet/node.py#L307 para:
# cmd = ['docker', 'exec', '-it', '-u', '0', '%s.%s' % (self.dnameprefix, self.name), 'env', 'PS1=' + chr(127),
~/containernet$ nano containernet/node.py

#Após isso, executar "sudo make install" no diretório raiz do containernet.
~/containernet$ sudo make install

# Executar os comandos abaixo para testar se a instalação do containernet
~/containernet$ cd containernet
~/containernet/containernet$ sudo python examples/containernet_example.py
containernet> d1 ifconfig 
```

### Configuração da do ambiente para teste de segurança de aplicações
A configuração da topologia está configurada no Containernet, devendo-se usar o script em python para que a configuração seja realilzada.

Código para geração da topologia no Containernet está no arquivo config_topologia.py, abaixo transcrito:

```python
#!/usr/bin/python
"""
Este é um script para subir os componentes da arquitetura da solução no Containernet, com as configurações necessárias
"""
from containernet.cli import CLI
#from containernet.link import TCLink
from containernet.net import Containernet
from mininet.node import Controller
from mininet.log import info, setLogLevel

import subprocess, os


def topologia():
   "Criando uma rede..."
   net = Containernet(controller=Controller, ipBase='10.100.0.0/24')
   #setLogLevel('info')
   #net = Containernet(controller=Controller)

   info('*** Adicionando os conteineres\n')
	# Criar o container do SonarQube
   sonar = net.addDocker('sonar',
      ip='10.100.0.125', 
      cpu_shares=20, privileged=True,
      volumes=["sonar_data:/opt/sonarqube/data",
         "sonar_extensions:/opt/sonarqube/extensions",
         "sonar_logs:/opt/sonarqube/logs"],
      dimage="ramonfontes/sonarqube:lts-community")

   # Criar o container do sonar em modo CLI
   sonar_cli = net.addDocker('sonar_cli',
      ip='10.100.0.120',
      cpu_shares=20, privileged=True,
      volumes=["app:/app"],
      dimage='ramonfontes/ubuntu:trusty')

   owasp_zap = net.addDocker('owasp_zap', 
      ip='10.100.0.140',
      cpu_shares=20, privileged=True,
      dimage="ramonfontes/zaproxy",		#atualizado o uso para essa versão por conta de ter mais recursos
      dcmd="zap.sh -daemon -config api.disablekey=true",
      volumes=["owasp_zap:/zap/wrk"])
   # complementação da configuração do OWASP ZAP
   owasp_zap.cmd('zap.sh --addoninstall soap')

   db_dvwa = net.addDocker('db_dvwa',
      ip='10.100.0.145', privileged=True,
      dimage="ramonfontes/mariadb:11",
      environment={'MYSQL_ROOT_PASSWORD':'dvwa','MYSQL_DATABASE':'dvwa','MYSQL_USER':'dvwa','MYSQL_PASSWORD':'p@ssw0rd'}, 
      volumes=["dvwa_db:/var/lib/mysql"])
   
   # Aplicação de teste DVWA
   dvwa = net.addDocker('dvwa',
      ip='10.100.0.150',
      port='4280:80', privileged=True,
      cpu_shares=20,
      #dimage="ramonfontes/dvwa:latest",
      # para tentar corrigir erro de IP e 404 file not found no repositório indicado acima
      dimage="marcelopinto350/dvwa:latest",
      environment={'DB_SERVER':"db_dvwa"})
      
   # Banco de dados da aplicação de segurança APPSEG
   appseg_db = net.addDocker('appseg_db',
      ip='10.100.0.155',
      #dimage="ramonfontes/postgres:alpine", privileged=True,
      # para substituir imagem acima para corrigir erro de IP
      dimage="marcelopinto350/postgres:alpine", privileged=True,
      environment={'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres',
         'POSTGRES_PORT':'5432'},
      volumes=["pg_data:/var/lib/postgresql/data"])
   
   # Aplicação de segurança APPSEG
   appseg = net.addDocker('appseg',
      ip='10.100.0.160',
      port='8000:8000', privileged=True,
      cpu_shares=20,
      #dimage="ramonfontes/python:3.10",
      # para corrigir erro de IP e na aplicação appseg
      dimage="marcelopinto350/appseg:alfa",
      environment={'POSTGRES_HOST':'appseg_db',
         'POSTRGES_PORT':'5432',
         'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres'},
      volumes=["appseg:/appseg"])

   info('*** Adicionando switches de rede\n')
   s1 = net.addSwitch('s1', failMode="standalone")

   info('*** Criando os links\n')
   net.addLink(sonar, s1)
   net.addLink(sonar_cli, s1)
   net.addLink(owasp_zap, s1)
   net.addLink(db_dvwa, s1)
   net.addLink(dvwa, s1)
   net.addLink(appseg_db, s1)

   info('*** Iniciando a rede\n')
   net.build()
   s1.start([])

   info('*** Executando CLI\n')
   CLI(net)

   info('*** Parando a rede...')
   net.stop()

if __name__ == '__main__':
   setLogLevel('info')
   topologia()
```


1. Clonar o arquivo e executar o scrip python
 ```shell
# Copiar o arquivo config_topologia.py
~$ mkdir app
~$ cd app
~/app$ nano config_topologia.py
# Colar o código deisponível acima e salvar o arquivo

# Executar o script para gerar a configuração inicial dos aplicativos
~/app$ sudo python config_topologia.py
 ```

2. Configurar o acesso ao banco de dados
Acessar o docker correspondente ao banco de dados da aplicação appseg_db e rodar a inicialização do bando de dados postgres 
```shell
# Executar o bash no docker do BD postgres da aplicação apseg
~$ docker exec -i mn.appseg_db bash
# na primeira vez executar esse comando 
appseg_db:/# docker-ensure-initdb.sh
appseg_db:/# su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'

```

3. Configurar o acesso ao Sonarqube
```shell
# executar o bash no docker do sonar
~$ docker exec -i mn.sonar bash
sonarqube@sonar:/opt/sonarqube$ docker/entrypoint.sh &

```
Acessar a aplicação pela navegador através do link <url>:<port>, por exemplo, 192.168.0.15:32785
3.1. Informar usuário e senha: admin/admin
3.2. indicar nova senha @dm1n e confirmar
3.3. Clicar em adicionar manualmente o projeto
   3.3.1. Indique o no do projeto
   3.3.2. Indique a chave única para o projeto no sonarqube
   3.3.3 Indique o nome da branch principal do projeto, por exemplo, master
   3.3.4 Clique no botão Set Up
3.4. Na página de configuração da integração da aplicação cliue em *Other CI*
   3.4.1 Clique no botão *Generate* para gerar um token para a aplicação e copie para cadastro no appseg, por exemplo, sqp_bd4affac00ce57c87e24b65544df7bbe821c2235.


4. configurar o acesso à linha de comando do Sonar (Sona_CLI)
Para ter acesso ao SonarCLI pela aplicação é necessário configurar uma chave de acesso para SSH da máquina da aplicação para a o container docker
4.1. Gerar a chave SSH, caso ainda não exista
```shell
~$ cd .ssh
~/.ssh$ ls
# Execute o comando abaixo, confirme o arquivo e deixe a senha em branco para gerar a chave
~/.ssh$ ssh-keygen -t rsa -b 4096
# copiar a chave pública para a outra máquina conforme o exemplo (ssh-copy-id usuario_remote@endereço_IP_remoto)
~/.ssh$ ssh-copy-id docker@192.168.0.15

```



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

