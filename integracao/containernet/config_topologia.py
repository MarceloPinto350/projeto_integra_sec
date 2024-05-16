#!/usr/bin/python
"""
Este é um script para subir o framework com as aplicações no containernet, de acordo com a topologia e
com as configurações necessárias ao funcionamento do framework.
"""
from containernet.cli import CLI
#from containernet.link import TCLink
from containernet.net import Containernet
from mininet.node import Controller
from mininet.log import info, setLogLevel


def monta_topologia():
   "Criando a rede para as ferramentas de verificação de segurança..."
   net = Containernet(controller=Controller)
   info('*** Adicionando um controlador\n')
   net.addController('c0')
   #net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

   info('*** Adicionando os hosts\n')
   h1 = net.addHost('h1', ip='10.100.0.2')
   h2 = net.addHost('h2', ip='10.100.0.20')

   #exemplos genéricos de como configurar containers
   #sast_container = net.addDocker('sast-container', ip='10.0.0.3', dimage='bandit_image')
   #sca_container = net.addDocker('sca-container', ip='10.0.0.4', dimage='dependency_check_image')
   #dast_container = net.addDocker('dast-container', ip='10.0.0.5', dimage='burp_suite_image')
   #iast_container = net.addDocker('iast-container', ip='10.0.0.6', dimage='jacoco_zap_image')
 
   info('*** Adicionando os conteineres\n')
   # postgres para aplicação bib
   #postgres_bib = net.addDocker('postgres_bib', 
   #  ip='10.100.0.100', 
   #  dimage="postgres:alpine",
   #  environment={'POSTGRES_DB':"bibpubdb",
   #     'POSTGRES_USER':"bibpub",
   #     'POSTGRES_PASSWORD':"@dm1n",
   #     'LANG':"pt_BR.UTF8",
   #     'PGDATA':"/var/lib/postgresql/data"})
   # aplicação bib
   #bib = net.addDocker('bib',
   #  ip='10.100.0.110', 
   #  dimage="marcelopinto350/bibpub:3.1",
   sonar = net.addDocker('sonar', 
      ip='10.100.0.120', 
      dimage="sonarqube:lts-community",       # usando a versão LTS (9.9.5) para fins de teste 
      volumes=["sonar_data:/opt/sonarqube/data",
         "sonar_extensions:/opt/sonarqube/extensions",
         "sonar_logs:/opt/sonarqube/logs"])
      #environment={'SONARQUBE_JDBC_URL':"jdbc:postgresql:/exit
      # /)
      
   # aplicação OWASP Dependency-Check - SCA
   owasp_dc = net.addDocker('owasp_dc', 
      ip='10.100.0.130',
      dimage="owasp/dependency-check:9.1.0",  # usando a versão 9.1.0 para fins de teste, porque é mais recente
      volumes=["owasp_dc:/src"],
      dcmd="dependency-check.sh -f ALL -s /src -o /src/report")
      #dcmd="--scan /src --format "ALL" --out /src/reports")
      
   # aplicação OWASP ZAP - DAST
   owasp_zap = net.addDocker('owasp_zap', 
      ip='10.100.0.140',      
      dimage="zaproxy/zap-bare:2.14.0",       # usando esta imagem para fins de teste, porque é mais leve
      #dimage="zaproxy/zap-stable",
      volumes=["owasp_zap:/zap/wrk"],
      dcmd="zap.sh -daemon -host http://10.100.0.140 -port 8000 -config api.disablekey=true")
   
   # aplicação XPTO - IAST
  
   info('*** Adicionando os volumes\n')
   #net.addVolume('pg_data', '/var/lib/postgresql/data')
   net.addVolume('sonar_data', '/opt/sonarqube/data')
   net.addVolume('sonar_extensions', '/opt/sonarqube/extensions')  
   net.addVolume('sonar_logs', '/opt/sonarqube/logs')
   net.addVolume('owasp_dc', '/src')       
   net.addVolume('owasp_zap', '/zap/wrk')
   #net.addVolume('iast', '/opt/iast')

   info('*** Criando os links entre as máquinas\n')
   #net.addLink(h1, postgres_bib)
   #net.addLink(h1, bib)
   net.addLink(h1, sonar)
   net.addLink(h1, owasp_dc)
   net.addLink(h1, owasp_zap)
   #net.addLink(h2, postgres_bib)
   #net.addLink(h2, bib)
   net.addLink(h2, sonar)
   net.addLink(h2, owasp_dc)
   net.addLink(h2, owasp_zap)
   
   info('*** Iniciando a rede\n')
   net.start()
   #net.build()
   #net.addNAT().configDefault()
   #s1.start([])

   info('*** Executando CLI\n')
   CLI(net)
 
   info('*** parando a rede')
   net.stop()


if __name__ == '__main__':
        setLogLevel('debug')
        monta_topologia()

