#!/usr/bin/python
"""
Este é um script para subir o sonarqube no containernet, com as configurações necessárias
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

   info('*** Adicinando um controlador\n')
   net.addController('c0')

   #exemplos genéricos de como configurar containers
   #sast_container = net.addDocker('sast-container', ip='10.0.0.3', dimage='bandit_image')
   #sca_container = net.addDocker('sca-container', ip='10.0.0.4', dimage='dependency_check_image')
   #dast_container = net.addDocker('dast-container', ip='10.0.0.5', dimage='burp_suite_image')
   #iast_container = net.addDocker('iast-container', ip='10.0.0.6', dimage='jacoco_zap_image')

   info('*** Adicionando os conteineres\n')
	# Criar o container do SonarQube
   sonar = net.addDocker('sonar',
      ip='10.100.0.125', 
      cpu_shares=20,
      volumes=["sonar_data:/opt/sonarqube/data",
         "sonar_extensions:/opt/sonarqube/extensions",
         "sonar_logs:/opt/sonarqube/logs"],
      dimage="sonarqube:lts-community")

   # Criar o container do sonar em modo CLI
   sonar_cli = net.addDocker('sonar_cli',
      ip='10.100.0.120',
      cpu_shares=20,
      volumes=["app:/app"],
      dimage='ubuntu:trusty')
      #dcmd="apt update && apt upgrade -y")
      #dcmd="wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip")
	# complementação da configuração do SonarQube em modo CLI
   info('*** Configurando sonarqube CLI ... \n')
   sonar_cli.cmd ('apt update && apt upgrade -y')
   sonar_cli.cmd ('apt install net-tools iputils-ping openssh-server openssl ca-certificates git zip -y')
	#config_sonar_cli ('sonar-scanner-cli-5.0.1.3006-linux.zip')
   info('*** Instalando o Sonarqube CLI ... \n')
   if not os.path.exists('sonar-scanner-cli-5.0.1.3006-linux.zip'):
      subprocess.run(f"wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip",shell=True)
   subprocess.run(f"docker cp sonar-scanner-cli-5.0.1.3006-linux.zip mn.sonar_cli:/tmp/sonar-scanner-cli-5.0.1.3006-linux.zip", shell=True)
   sonar_cli.cmd("unzip /tmp/sonar-scanner-cli-5.0.1.3006-linux.zip")
   sonar_cli.cmd(f"mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner")
   sonar_cli.cmd("ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/bin/sonar-scanner") 

	
	# configuração do  container do owasp_zap
   owasp_zap = net.addDocker('owasp_zap', 
      ip='10.100.0.140',
      cpu_shares=20,
		#dimage="zaproxy/zap-bare:2.14.0",       # usando esta imagem para fins de teste, porque é mais leve (é muito restrita)
      dimage="zaproxy/zap-stable",		#atualizado o uso para essa versão por conta de ter mais recursos
		#dcmd="zap.sh -daemon -host http://10.100.0.140 -port 8000 -config api.disablekey=true",
		#dcmd="zap.sh --addoninstall soap",
		#dcmd="zap.sh -daemon -host http://172.17.0.3 -config api.disablekey=true",
      dcmd="zap.sh -daemon -config api.disablekey=true",
      volumes=["owasp_zap:/zap/wrk"])
   # complementação da configuração do OWASP ZAP
   owasp_zap.cmd('zap.sh --addoninstall soap')

   # aplicação OWASP Dependency-Check - SCA
#   owasp_dc = net.addDocker('owasp_dc', 
#      ip='10.100.0.130',
#      cpu_shares=20,
#      dimage="owasp/dependency-check:9.1.0",  # usando a versão 9.1.0 para fins de teste, porque é mais recente
#      #dcmd="dependency-check.sh -f ALL -s /src -o /src/report",
#      #dcmd="--scan /src --format "ALL" --out /src/reports",
#      volumes=["owasp_dc:/src"])


   # Banco de dados para a aplicação de teste DVWA
   db_dvwa = net.addDocker('db_dvwa',
      ip='10.100.0.145',
      dimage="docker.io/library/mariadb:10",
      environment={'MYSQL_ROOT_PASSWORD':'dvwa','MYSQL_DATABASE':'dvwa','MYSQL_USER':'dvwa','MYSQL_PASSWORD':'p@ssw0rd'}, 
      volumes=["dvwa_db:/var/lib/mysql"])
   
   # Aplicação de teste DVWA
   dvwa = net.addDocker('dvwa',
      ip='10.100.0.150',
      port='4280:80',
      cpu_shares=20,
      dimage="ghcr.io/digininja/dvwa:latest",
      environment={'DB_SERVER':"db_dvwa"})

      
   # Banco de dados da aplicação de segurança APPSEG
   appseg_db = net.addDocker('appseg_db',
      ip='10.100.0.155',
      dimage="postgres:alpine",
      environment={'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres',
         'POSTGRES_PORT':'5432'},
      volumes=["pg_data:/var/lib/postgresql/data"])
   
   
   # Aplicação de segurança APPSEG
   appseg = net.addDocker('appseg',
      ip='10.100.0.160',
      port='8000:8000',
      cpu_shares=20,
      dimage="python:3.10",
      environment={'POSTGRES_HOST':'appseg_db',
         'POSTRGES_PORT':'5432',
         'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres'},
      volumes=["appseg:/appseg"])
   
   info('*** Configurando sonarqube CLI ... \n')
   appseg.cmd ('apt update && apt upgrade -y')
   appseg.cmd ('apt install -y linux-headers net-tools \
      apt-transport-https ca-certificates curl openssh-server \
      openssl postgresql-client iputils-ping setuptools')
   
   info('*** Instalando a aplicação appseg... \n')
   if not os.path.exists('/home/docker/projeto_integra_sec/'):
      appseg.cappseg.cmd ("cd /home/docker/")
      subprocess.run("git clone https://github.com/MarceloPinto350/projeto_integra_sec.git")
   subprocess.run("docker cp projeto_integra_sec/ mn.appsec:/.", shell=True)
   appseg.cappseg.cmd ("cd projeto_integra_sec")   
   appseg.cmd ("python3 -m venv venv")        # configura as configurações de ambiente com o venv
   appseg.cmd ("source venv/bin/activate")    # para ativar o venv - observe que irá ficar com o texto (venv) no início do prompt
   appseg.cmd ('pip install -U pip')
   appseg.cmd ("pip install -r requirements.txt")
   appseg.cmd ("python manage.py runserver 0.0.0.0:8000")
   #appseg.cmd("python manage.py makemigrations")
   #appseg.cmd("python manage.py migrate")
   #appseg.cmd("python manage.py createsuperuser")
    
#   info('*** Adicionando os volumes\n')
#   #net.addVolume('pg_data', '/var/lib/postgresql/data')
#   net.addVolume('sonar_data', '/opt/sonarqube/data')
#   net.addVolume('sonar_extensions', '/opt/sonarqube/extensions')  
#   net.addVolume('sonar_logs', '/opt/sonarqube/logs')
#   net.addVolume('owasp_dc', '/src')       
#   net.addVolume('owasp_zap', '/zap/wrk')
#   #net.addVolume('iast', '/opt/iast')


#	#d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
	
	#info('*** Adicinando os volumes de dados\n')
#	net.addVolume('owasp_dc', '/src')

	# instalando e executando outros comandos nos containers
#	owasp_zap.cmd('zap.sh -daemon -host http://172.17.0.3 -config api.disablekey=true &')
#  owasp_zap.cmd('zap.sh --addoninstall soap')
#	sonar_cli.cmd ('apt update && apt upgrade -y')
#	sonar_cli.cmd ('apt install net-tools iputils-ping openssh-server openssl ca-certificates git -y')


	info('*** Adicionando switches de rede\n')
	s1 = net.addSwitch('s1', failMode="standalone")
	#s2 = net.addSwitch('s2')

	#info('*** Adicionando os hosts\n')
	#h1 = net.addHost('h1', ip='10.100.0.2')
	#h2 = net.addHost('h2', ip='10.100.0.20')

	info('*** Criando os links\n')
	#net.addLink(h1, s1)
	#net.addLink(h2, s1)
	net.addLink(sonar, s1)
	net.addLink(sonar_cli, s1)
	net.addLink(owasp_zap, s1)
   net.addLink(db_dvwa, s1)
   net.addLink(dvwa, s1)
   net.addLink(appseg_db, s1)
	#net.addLink(h2, s1)
	#net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
	#net.addLink(s1, bibpub)

	info('*** Iniciando a rede\n')
	net.build()
#	net.addNAT().configDefault()
	s1.start([])

	info('*** Executando CLI\n')
	CLI(net)

	info('*** Parando a rede...')
	net.stop()


#def config_sonar_cli(arquivo):
#   "Configurando o SonarQube em modo CLI" 
#   if not os.path.exists(f"{arquivo}"):
#      subprocess.run(f"wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/{arquivo}",shell=True)
#   subprocess.run(f"docker cp {arquivo} mn.sonar_cli:/tmp/{arquivo}", shell=True)
#   #info(f"Resultado: {subprocess.run(ls /tmp/{arquivo}, shell=True, stdout=subprocess.PIPE)")
#   #if subprocess.run(f"ls /tmp/{arquivo}", shell=True, stdout=subprocess.PIPE) == 0:
#   #   print(f"Arquivo /tmp/{arquivo} existe no container...")
#   #   # descompactando o arquivo no container
#   #   #subprocess.run(f"unzip /tmp/{arquivo}", shell=True, stdout=subprocess.PIPE)
#   sonar_cli.cmd("cd /tmp && unzip /tmp/{arquivo}")
#   #   #subprocess.run("mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner",shell=True)
#   sonar_cli.cmd(f"mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner")
#   #   #subprocess.run("ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/bin/sonar-scanner", shell=True)
#   sonar_cli.cmd("ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/bin/sonar-scanner") 
#   #   #subprocess.run(f"rm -rf tmp/'{arquivo}'")
#   #   #sonar_cli.cmd(f"rm -rf /tmp/{arquivo}") 
#   #   print(f"Arquivo /tmp/{arquivo} descompactado no container")
#   #else:
#   #   print(f"Arquivo /tmp/{arquivo} NÃO existe no container...")




if __name__ == '__main__':
   setLogLevel('debug')
   topologia()
