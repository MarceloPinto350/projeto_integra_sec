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
      #dimage="ramonfontes/zaproxy",		#atualizado o uso para essa versão por conta de ter mais recursos
      dimage="marcelopinto350/owasp_zap",
      #dcmd="zap.sh -daemon -config api.disablekey=true",
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","owasp_zap:/zap/wrk"])
   
   # Criar o container do Owasp dependency-check
   owasp_dc = net.addDocker('owasp_dc',
      ip='10.100.0.135',
      cpu_shares=20, privileged=True,
      environment={'DISPLAY':":0"},
      #dimage="marcelopinto350/owasp-dependency-check:9.2",
      dimage="marcelopinto350/owasp_dc:9.2",
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
      environment={'DISPLAY':":0"},
         # 'POSTGRES_DB':'appseg',
         # 'POSTGRES_USER':'postgres',
         # 'POSTGRES_PASSWORD':'postgres',
         # 'POSTGRES_PORT':'5432'},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","pg_data:/var/lib/postgresql/data"])
   
   # Criar a aplicação de segurança APPSEG
   appseg = net.addDocker('appseg',
      ip='10.100.0.155',
      port='8000:8000', privileged=True,
      cpu_shares=20,
      #dimage="ramonfontes/python:3.10",
      dimage="marcelopinto350/appseg:beta",
      environment={'DISPLAY':":0",
         'POSTGRES_HOST':'10.100.0.150',
         'POSTRGES_PORT':'5432',
         'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres',
         'URL_API':'http://10.100.0.155:8000/api'},
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
