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
      dimage="ramonfontes/dvwa:latest",
      environment={'DB_SERVER':"db_dvwa"})
      
   # Banco de dados da aplicação de segurança APPSEG
   appseg_db = net.addDocker('appseg_db',
      ip='10.100.0.155',
      dimage="ramonfontes/postgres:alpine", privileged=True,
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
      dimage="ramonfontes/python:3.10",
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
