# O ambiente

O ambiente para realização da prova de conceito para a solução de segurança de software AppSeg possui a seguinte composição:

1. Containetnet - para suportar as configurações das ferramentas de análise de segurança

   * 1.1. **SAST - SonarQube (sonar)** - servidor da ferramenta Sonar Qube, para análise estática do código fonte das aplicações (SAST)

   * 1.2. **(sonar_cli)** - é a máquina responsável pela intercomunicação da Aplicação de Análise de Segurança e o Sonar Qube, via linha de comando

   * 1.3. **DAST: OWASP ZAP (owasp_zap)** - servidor da ferramenta OWASP-ZAP, para análise dinâmica das apliações (DAST)

   * 1.4. **SCA: OWASP Dependençy Check (owasp_dc)** - servidor da ferramenta OWASP Dependency Check, para análise de dependência de bibliotecas de terceiros (SCA)

   * 1.5. **Damn Vulnerable Web Application (DVWA)** - é uma aplicação web desenvolvida PHP + MySQL com a finalidade de realização de testes e praticar seurança com algumas das mais comuns vulnerabilidades web, com vários níveis de dificuldade; Disponível no repositório do Github: <https://github.com/digininja/DVWA.git>.

2. Aplicação AppSeg e banco de dados postgres - disponibilização da aplicação WEB e API para cadastro das aplicações e suas configurações, integração dos resultados de análise de vulnerabilidades e controle de chamadas às ferramentas de análise de segurança.

## Preparação do ambiente da POC

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

O Containernet é um fork do Mininet, um emulador de redes que possibilita o uso de container Docker em topologias de rede, sendo usado ativamente pela comunidade de pesquisa, com foco em experimentos no campo de Cloud Computing, Fog Computing, Network Functoin Virtualization (NFV) e Multi-access Edge Computing computação (MEC). Para configuração do Containernet é necessário acessar a máquina virtual, através de SSH, e proceder os seguintes passos para atualização do servidor e preparação do ambiente:

```shell
# Atualizar as configurações da máquina e intalar o Git e o Ansible
~$ sudo apt update && sudo apt upgrade -y && sudo apt install vim nano git ansible -y

# Clonar e instalar o containernet 
~$ git clone https://github.com/ramonfontes/containernet.git

# Proceder a instalação do containernet
~$ cd containernet
~/containernet$ sudo util/install.sh -W

#Caso necessário, confirmar eventuais necessidades de reinicialização de serviços.

#Em caso de erros, verificar e ajustar configuração do containernet, para integração do ambiente, conforme indicado:

#1. editar o arquivo: 
   ~/containernet$ nano containernet/node.py

#2. alterar linha containernet/node.py#L304 para:
   cmd = ['docker', 'exec', '-it', '-u', '0', '%s' % self.did, 'env', 'PS1=' + chr(127),

#3. alterar linha containernet/node.py#L307 para:
   cmd = ['docker', 'exec', '-it', '-u', '0', '%s.%s' % (self.dnameprefix, self.name), 'env', 'PS1=' + chr(127),   

#4. em seguida executar "sudo make install" no diretório raiz do containernet.
   ~/containernet$ sudo make install

# Executar os comandos abaixo para testar se a instalação do containernet
~/containernet$ cd containernet
~/containernet/containernet$ sudo python examples/containernet_example.py
containernet> d1 ifconfig 
```

### Configuração do ambiente para teste de segurança de aplicações

A configuração da topologia para o Containernet deverá feita através da execução do script em python, conforme o arquivo **config_topologia.py**, abaixo transcrito:

```python
#!/usr/bin/python
"""
Este é um script para subir os componentes da arquitetura da solução no Containernet, com as configurações necessárias

alterar linha https://github.com/ramonfontes/containernet/blob/master/containernet/node.py#L304 para cmd = ['docker', 'exec', '-it', '-u', '0, '%s' % self.did, 'env', 'PS1=' + chr(127),
alterar linha https://github.com/ramonfontes/containernet/blob/master/containernet/node.py#L307 para cmd = ['docker', 'exec', '-it', '-u', '0, '%s.%s' % (self.dnameprefix, self.name), 'env', 'PS1=' + chr(127),
Após isso, executar "sudo make install" no diretório raiz do containernet.

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
   #Criar o container do SonarQube
   sonar = net.addDocker('sonar',
      ip='10.100.0.120', 
      cpu_shares=20, privileged=True,
      environment={'DISPLAY':":0"},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw",
         "sonar_data:/opt/sonarqube/data",
         "sonar_extensions:/opt/sonarqube/extensions",
         "sonar_logs:/opt/sonarqube/logs"],
      dimage="ramonfontes/sonarqube:lts-community")

   # Criar o container do sonar em modo CLI
   sonar_cli = net.addDocker('sonar_cli',
      ip='10.100.0.125',
      cpu_shares=20, privileged=True,
      environment={'DISPLAY':":0"},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","app:/app"],
      dimage='ramonfontes/ubuntu:trusty')

   # Criar o container do OWASP ZAP
   owasp_zap = net.addDocker('owasp_zap', 
      ip='10.100.0.130',
      cpu_shares=20, privileged=True,
      environment={'DISPLAY':":0"},
      dimage="ramonfontes/zaproxy",    #atualizado o uso para essa versão por conta de ter mais recursos
      #dcmd="zap.sh -daemon -config api.disablekey=true",
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","owasp_zap:/zap/wrk"])
   
   # Criar o container do Owasp dependency-check
   owasp_dc = net.addDocker('owasp_dc',
      ip='10.100.0.135',
      cpu_shares=20, privileged=True,
      environment={'DISPLAY':":0"},
      dimage="marcelopinto350/owasp-dependency-check:9.2",
      #dcmd="--scan /src --format 'JSON' --out /src/report",
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","owasp_dc:/src"])

   # Criar o container do BD da aplicação de teste DVWA
   dvwa_db = net.addDocker('dvwa_db',
      ip='10.100.0.140', privileged=True,
      dimage="ramonfontes/mariadb:11",
      environment={'DISPLAY':":0",'MYSQL_ROOT_PASSWORD':'dvwa','MYSQL_DATABASE':'dvwa','MYSQL_USER':'dvwa','MYSQL_PASSWORD':'p@ssw0rd'}, 
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","dvwa_db:/var/lib/mysql"])
   
   # Criar o container da aplicação de teste DVWA
   dvwa = net.addDocker('dvwa',
      ip='10.100.0.145',
      port='4280:80', privileged=True,
      cpu_shares=20,
      #dimage="ramonfontes/dvwa:latest",
      #dimage="marcelopinto350/dvwa:latest",
      dimage="ramonfontes/xss_attack",
      #volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","dvwa:/var/www/html"],
      environment={'DISPLAY':":0",'DB_SERVER':"dvwa_db"})
      
   # Criar o BD da aplicação de segurança APPSEG
   appseg_db = net.addDocker('appseg_db',
      ip='10.100.0.150',
      #dimage="ramonfontes/postgres:alpine", privileged=True,
      dimage="marcelopinto350/postgres:alpine", privileged=True,
      environment={'DISPLAY':":0",
         'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres',
         'POSTGRES_PORT':'5432'},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","pg_data:/var/lib/postgresql/data"])
   
   # Criar a aplicação de segurança APPSEG
   appseg = net.addDocker('appseg',
      ip='10.100.0.155',
      port='8000:8000', privileged=True,
      cpu_shares=20,
      #dimage="ramonfontes/python:3.10",
      dimage="marcelopinto350/appseg:alfa",
      environment={'DISPLAY':":0",
         'POSTGRES_HOST':'appseg_db',
         'POSTRGES_PORT':'5432',
         'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres'},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","appseg:/appseg"])

   info('*** Adicionando switches de rede\n')
   s1 = net.addSwitch('s1', failMode="standalone")

   info('*** Criando os links\n')
   net.addLink(sonar, s1)
   net.addLink(sonar_cli, s1)
   net.addLink(owasp_zap, s1)
   net.addLink(owasp_dc, s1)
   net.addLink(dvwa_db, s1)
   net.addLink(dvwa, s1)
   net.addLink(appseg_db, s1)
   net.addLink(appseg, s1)
   info('*** Iniciando a rede\n')
   net.build()
   s1.start([])

   # complementação das configurações e execuções posteriores 
   
   # Instalar e configurar o servidor ssh nas máquinas SOANR_CLI, OWASP_DC e OWASP_ZAP
   info('*** Configurando os containers\n')
   sonar_cli.cmd('sed -i "s/PermitRootLogin without-password/PermitRootLogin yes/g" /etc/ssh/sshd_config')
   sonar_cli.cmd('service ssh start')
   #
   owasp_dc.cmd('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
   owasp_dc.cmd('service ssh start')
   #
   owasp_zap.cmd('apt-get update && apt-get install -y openssh-server vim')
   owasp_zap.cmd('service ssh start')
   
   # mudar as senhas dos usuários root e zap para "root" e "zap" respectivamente
   sonar_cli.cmd('echo root:root | chpasswd')
   owasp_dc.cmd('echo "root:root" | chpasswd')
   owasp_zap.cmd('echo "zap:zap" | chpasswd')
      
   # Inicializar o postgresql
   appseg_db.cmd("su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'")
   
   # Incializar o sonarqube
   sonar.cmd("su sonarqube -c 'docker/entrypoint.sh &'")
   
   # configurar o owasp_dc
   owasp_dc.cmd('echo export JAVA_OPTION="Xmx2g" >> ~/.bashrc')
   
   # Inicializar o owasp zap colocando a pasta de trabalho como sendo de propriedade do usuário zap
   owasp_zap.cmd('chown -R zap:zap wrk')
   
   # Subir o BD da aplicação de teste DVWA
   #dvwa_db.cmd('service mariadb start')
   #dvwa_db.cmd('docker-entrypoint.sh mysqld &')
   
   # Rodar a aplicação de teste DVWA
   dvwa.cmd('sh main.sh &')   
   
   # Subir a aplicação AppSeg
   appseg.cmd('cd /appseg & python3 manage.py runserver 0.0.0.0:8000 &')
   
 
   info('*** Executando CLI\n')
   CLI(net)

   info('*** Parando a rede...')
   net.stop()

if __name__ == '__main__':
   #setLogLevel('info')
   setLogLevel('debug')
   topologia()

```

### Finalização da configuração do ambiente de teste

Para finalização da configuração do ambiente, proceder as execução dos passos a seguir:

1. Clonar o arquivo e executar o script python

```shell
# Copiar o arquivo config_topologia.py
~$ mkdir app
~$ cd app
~/app$ nano config_topologia.py
# Colar o código disponível acima e salvar o arquivo

# Executar o script para gerar a configuração inicial dos aplicativos
~/app$ sudo python config_topologia.py
 ```

2.Configurar o acesso ao banco de dados
Acessar o docker correspondente ao banco de dados da aplicação appseg_db e rodar a inicialização do bando de dados postgres

```shell
# Executar o bash no docker do BD postgres da aplicação appseg
~$ docker exec -it mn.appseg_db bash
# na primeira vez executar esse comando 
appseg_db:/# docker-ensure-initdb.sh
appseg_db:/# su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'
```

ou diretamente através do Containernet:

containernet> appseg_db docker-ensure-initdb.sh
containernet> appseg_db su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'

3.Configurar a aplicação APPSEG para utilizar o banco de dados
Acessar o docker correspondente à Aplicação APPSEG e executar os comandos a seguir:

```shell
# Executar o bash no docker da aplicação APPSEG
~$ docker exec -it mn.appseg bash
# na primeira vez executar esse comando 
appseg:/# python manage.py makemigrations
appseg:/# python manage.py migrate
# criar o usuário adminsitrador da aplicação
appseg:/# python manage.py createsuperuser
# executar a aplicação
appseg:/# python manage.py runserver 0.0.0.0:8000

## Configurar acesso aos servidores do sonar_cli, owasp_dc e owasp_zap via SSH
appseg:/#  ssh root@10.100.0.125 
# Sonar_cli: aceitar conexão; senha root
appseg:/#  ssh root@10.100.0.130 
# Owasp_dc: aceitar conexão; senha root
appseg:/#  ssh zap@10.100.0.135 
# Owasp_zap: aceitar conexão; senha zap
```

ou diretamente através do Containernet:

containernet> appseg python manage.py makemigrations
containernet> appseg python manage.py migrate
containernet> appseg python manage.py createsuperuser
containernet> appseg python manage.py runserver 0.0.0.0:8000

4.Configurar o acesso ao Sonarqube

```shell
# executar o bash no docker do sonar
~$ docker exec -i mn.sonar bash
sonarqube@sonar:/opt/sonarqube$ docker/entrypoint.sh &
```

ou diretamente através do Containernet:

containernet> sonar docker/entrypoint.sh &

### Teste de acesso à aplicação

Para verificar se o ambiente está acessível, acessar a aplicação pela navegador através do link \<url>:\<porta>/admin, por exemplo, 192.168.0.15:32771/admin, onde:

**\<url>**: é o endereço do host do containernet;

**\<porta>**: é a porta gerada para a aplicação APPSEG pelo containernet

### Outras configurações

Outras configurações necessárias para realizações de testes

1. Inclusão de projeto da aplicação a ser testado no SonarQube

1.1. Informar usuário e senha: admin/admin

1.2. Indicar nova senha @dm1n e confirmar

1.3. Clicar em adicionar manualmente o projeto

   1.3.1. Indique o nome do projeto

   1.3.2. Indique a chave única para o projeto no sonarqube

   1.3.3. Indique o nome da branch principal do projeto, por exemplo, master

   1.3.4. Clique no botão Set Up

1.4. Na página de configuração da integração da aplicação clique em *Other CI*

   1.4.1 Clique no botão *Generate* para gerar um token para a aplicação e copie para cadastro no appseg, por exemplo, sqp_bd4affac00ce57c87e24b65544df7bbe821c2235.

2.Configurar o acesso direto à linha de comando do Sonar (Sonar_CLI)
Para ter acesso ao SonarCLI pela aplicação AppSeg é necessário configurar uma chave de acesso para SSH da máquina da aplicação para a o container docker

2.1. Entrar na máquina da APPSEG e gerar a chave SSH da máquina onde a aplicação está sendo executada, caso ainda não exista

```shell
~$ cd .ssh
~/.ssh$ ls -lah   # lista os arquivos existentes na pasta
# Execute o comando abaixo, confirme o arquivo e deixe a senha em branco para gerar a chave
~/.ssh$ ssh-keygen -t rsa -b 4096
# copiar a chave pública para a outra máquina conforme o exemplo (ssh-copy-id usuario_remote@endereço_IP_remoto)
~/.ssh$ ssh-copy-id docker@192.168.0.15
```

2.2. Gerar token de autenticação do(s) usuário(s) que irá(ão) acessar os serviços web, caso seja de interesse:

a) Acessar a aplicação pelo navegador de sua preferência, por exemplo, 192.160.0.24:8000/admin

b) Informar usuário e senha de acesso;

c) Selecionar a opção **Tokens >> + Adicionar**;

d) Selecionar o usuário e clicar no botão **Salvar**;

e) Caso queira, é possível clicar no ícone **+**, ao lado da caixa de seleção de usuário, para adicionar novos usuários.

### Fazer o deploy da aplicação

**1º Passo**: Clonar o projeto do github para a pasta local

```shell
git clone https://github.com/MarceloPinto350/projeto_integra_sec.git
```

**2º Passo**: Executar o comando para criação de imagem:

```shell
# executar o comando onde estiver o arquivo Dockerfile
~/projeto_integra_seg$ docker build -t appseg:<versao> .
```

**3º Passo**: Executar a aplicação para se certificar que está tudo ok

```shell
~/projeto_integra_seg$ docker run -it  --name appseg-<versao> -p 8000:8000 appseg:<versao>
```

**4º Passo**: Criar tag da imagem para enviar para repositório remoto

```shell
~/projeto_integra_seg$ docker tag appseg:<versao> marcelopinto350/appseg:<versao>
```

**5º Passo**: Conectar na conta do repositório (git)

```shell
~/projeto_integra_seg$ docker login
```

Informar usuário e senha, conforme o caso.

**5º Passo**: Enviar dados para repositório

```shell
~/projeto_integra_seg$ docker push marcelopinto350/appseg:beta
```

### Criar uma imagem a partir de um container

```shell
# criar um conainer a aprtir de uma imagem base, conforme o exemplo
$ docker run -it --name owasp_dc marcelopinto350/owasp-dependency-check:9.2 bash

# dentro do container fazer as atualizações de interesse
9388204# apt update && apt upgrade -y
9388204# apt install -y nano openssh-server
9388204# exit

# criar a imagem a partir do container que está visiível através do comando docker ps -a
$ docker commit owasp_dc owasp_dc:9.2

# criar a tag
$ docker tag owasp_dc:9.2 marcelopinto350/owasp_dc:9.2

# conectar no repositório
$ docker login

# enviar imagem para o repositório
$ docker push marcelopinto350/owasp_dc:9.2

**Outros comando importantes**

Remover uma imagem existente localmente: $ docker rmi appseg:beta

Configurar o SSH server nos hosts
=================================
**SONAR_CLI**
```shell
$ docker exec -it mn.sonar_cli bash
#root@sonar_cli:/# apt update && apt install openssh-server vim -y
root@sonar_cli:/# service ssh start

# Através do containernet
#containernet> sonar_cli apt update && apt install openssh-server vim -y
containernet> sonar_cli service ssh start
```

**OWASP_DC** Subir o serviço SSH.

```shell
$ docker exec -it mn.owasp_dc bash
#root@owasp_dc:/# apt update && apt install openssh-server vim -y
root@owasp_dc:/# service ssh start

# Através do containernet
#containernet> owasp_dc apt update && apt install openssh-server vim -y
containernet> owasp_dc service ssh start
```

**OWASP_ZAP** Subir o serviço de SSH

```shell
$ docker exec -it mn.owasp_zap bash
#root@owasp_zap:/# apt update && apt install openssh-server -y
root@owasp_zap:/# service ssh start

# Através do containernet
#containernet> owasp_zap apt update && apt install openssh-server -y
containernet> owasp_zap service ssh start
```

**APPSEG** Necesário configurar o acesso do servdor appseg para as demais máquinas via SSH direto, sendo necessário eventualmente ajustar em cada servidor a permissão para conectar via SSH ao usuário root, para os conforme o caso.

## Outros ações necessárias para habilitar o ambinete de caso de testes

### Instalar certificado do TRT na Máquina Virtual do containernet

```shell
# Copiar o arquivo .crt para o servidor
~/Download>$ sudo cp certificado.crt /usr/local/share/ca-certificates

# sincronizar os dados do repositório do ca-certificates
~/Download>$ sudo dpkg-reconfigure ca-certificates

# instalar os certificados copiados para a pasta local
~/Download>$ sudo update-ca-certificates
```
