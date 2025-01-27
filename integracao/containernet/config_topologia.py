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
      #ipbase='172.17.0.0/24',
      port='9000:9000',
      port_bindings={9000:9000},
      publish_all_ports=True,
      cpu_shares=20, 
      privileged=True,
      environment={'DISPLAY':":0"},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw",
         "sonar_data:/opt/sonarqube/data",
         "sonar_extensions:/opt/sonarqube/extensions",
         "sonar_logs:/opt/sonarqube/logs"],
      dimage="ramonfontes/sonarqube:lts-community")

   # Criar o container do sonar em modo CLI
   sonar_cli = net.addDocker('sonar_cli',
      ip='10.100.0.125',
      #ipbase='172.17.0.0/24',
      cpu_shares=20, 
      privileged=True,
      environment={'DISPLAY':":0"},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","app:/app"],
      #dimage='ramonfontes/ubuntu:trusty')
      dimage='marcelopinto350/sonarcli-ubuntu:trusty')

   # Criar o container do OWASP ZAP
   owasp_zap = net.addDocker('owasp_zap', 
      ip='10.100.0.130',
      #ipbase='172.17.0.0/24',
      cpu_shares=20, 
      privileged=True,
      environment={'DISPLAY':":0"},
      #dimage="ramonfontes/zaproxy",		#atualizado o uso para essa versão por conta de ter mais recursos
      dimage="marcelopinto350/owasp_zap",
      #dcmd="zap.sh -daemon -config api.disablekey=true",
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","owasp_zap:/zap/wrk"])
   
   # Criar o container do Owasp dependency-check
   owasp_dc = net.addDocker('owasp_dc',
      ip='10.100.0.135',
      #ipbase='172.17.0.0/24',
      cpu_shares=20, 
      privileged=True,
      environment={'DISPLAY':":0"},
      dimage="marcelopinto350/owasp_dc:9.2",
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","owasp_dc:/src"])

   # Criar o container do BD da aplicação de teste DVWA
   dvwa_db = net.addDocker('dvwa_db',
      ip='10.100.0.140', 
      #ipbase='172.17.0.0/24',
      dimage="ramonfontes/mariadb:11",
      environment={'DISPLAY':":0",
            'MYSQL_ROOT_PASSWORD':'dvwa',
            'MYSQL_DATABASE':'dvwa',
            'MYSQL_USER':'dvwa',
            'MYSQL_PASSWORD':'p@ssw0rd'}, 
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","dvwa_db:/var/lib/mysql"])
   
   # Criar o container da aplicação de teste DVWA
   dvwa = net.addDocker('dvwa',
      ip='10.100.0.145',
      #ipbase='172.17.0.0/24',
      port='4280:80', 
      port_bindings={4280:80},
      publish_all_ports=True,
      privileged=True,
      cpu_shares=20,
      #dimage="ramonfontes/dvwa:latest",
      dimage="ramonfontes/xss_attack",
      environment={'DISPLAY':":0",'DB_SERVER':"dvwa_db"})
      
   # Criar o BD da aplicação de segurança APPSEG
   appseg_db = net.addDocker('appseg_db',
      ip='10.100.0.150',
      #ipbase='172.17.0.0/24',
      port='5432:5432',
      port_bindings={5432:5432},
      publish_all_ports=True,
      #dimage="ramonfontes/postgres:alpine", privileged=True,
      dimage="marcelopinto350/postgres:alpine", 
      privileged=True,
      environment={'DISPLAY':":0"},
      volumes=["/tmp/.X11-unix:/tmp/.X11-unix:rw","pg_data:/var/lib/postgresql/data"])
   
   # Criar a aplicação de segurança APPSEG
   appseg = net.addDocker('appseg',
      ip='10.100.0.155',
      #ipbase='172.17.0.0/24',
      port='8000:8000', 
      port_bindings={8000:8000},
      publish_all_ports=True,
      privileged=True,
      cpu_shares=20,
      dimage="marcelopinto350/appseg:beta",
      environment={'DISPLAY':":0",
         'POSTGRES_HOST':'10.100.0.150',
         'POSTRGES_PORT':'5432',
         'POSTGRES_DB':'appseg',
         'POSTGRES_USER':'postgres',
         'POSTGRES_PASSWORD':'postgres',
         'URL_API':'http://10.100.0.155:8000/api',
         'SENHA_SERVICO':'@dm1n'},
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
   #owasp_zap.cmd('apt-get update && apt-get install -y openssh-server nano')
   owasp_zap.cmd('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
   owasp_zap.cmd('service ssh start')
   
   # mudar as senhas dos usuários root e zap para "root" e "zap" respectivamente
   sonar_cli.cmd('echo root:root | chpasswd')
   owasp_dc.cmd('echo "root:root" | chpasswd')
   owasp_zap.cmd('echo "zap:root" | chpasswd')
      
   # Inicializar o postgresql
   appseg_db.cmd("su postgres -c 'pg_ctl start -D /var/lib/postgresql/data'")
   
   # Incializar o sonarqube
   sonar.cmd("chown -R sonarqube:sonarqube /opt/sonarqube/")
   sonar.cmd("su sonarqube -c 'docker/entrypoint.sh &'")
   
   # configurar o owasp_dc
   owasp_dc.cmd('echo export JAVA_OPTION="Xmx2g" >> ~/.bashrc')
   
   # Inicializar o owasp zap colocando a pasta de trabalho como sendo de propriedade770 do usuário zap
   owasp_zap.cmd('chown -R zap:zap wrk')
   
   # Rodar a aplicação de teste DVWA
   dvwa.cmd('sh main.sh &')   
   
   # Subir a aplicação AppSeg
   appseg.cmd('python3 manage.py migrate')
   appseg.cmd('python3 manage.py runserver 0.0.0.0:8000 &')
   
   # configuração específica para o permitir aesso às aplicaçãoes via host local do docker
   #appseg.cmd("route add -net 172.17.0.0 netmask 255.255.0.0 gw 172.17.0.1 "
   
   # Exemplos/modelos de comandos para processar varredura, no Sonar, Owasp-dc e Owasp-zap, respectivamente
   # 1. sonar_cli.cmd('sonar-scanner -X -Dsonar.projectKey={aplicacao} -Dsonar.sources={aplicacao} -Dsonar.host.url={url_app} -Dsonar.token={app_token} -Dsonar.login={user} -Dsonar.password={password} -Dsonar.exclusions=**/*.java')
   # 2. owasp_dc.cmd('/bin/dependency-check.sh --project {aplicacao} --scan /src/{aplicacao} --format JSON --out {report_path}/{aplicacao} -n')
   # 3. owasp_zap.cmd('python zap-full-scan.py -t  {url_app} -J {report_path}/owasp_zap_report_{aplicacao}.json -d')
 
   info('*** Executando CLI\n')
   CLI(net)

   info('*** Parando a rede...')
   net.stop()

if __name__ == '__main__':
   #setLogLevel('info')
   setLogLevel('debug')
   topologia()
