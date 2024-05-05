#!/usr/bin/python
"""
Este é um script para subir as aplicações mo containernet, com as configurações necessárias
"""
from containernet.cli import CLI
from containernet.link import TCLink
from containernet.net import Containernet
from mininet.node import Controller
from mininet.log import info, setLogLevel


def topology():
	"Crinado uma rede."
	net = Containernet(ipBase='10.100.0.0/24')
	#setLogLevel('info')
	#net = Containernet(controller=Controller)
	#info('*** Adicinando um controlador\n')
	#net.addController('c0')
	info('*** Adicionando os conteineres\n')
	pgbib = net.addDocker('pgbib', 
		environment={'POSTGRES_DB':"bibpubdb",
                        'POSTGRES_USER':"bibpub",
                        'POSTGRES_PASSWORD':"@dm1n",
                        'LANG':"pt_BR.UTF8",
                        'PGDATA':"/var/lib/postgresql/data"},
		ip='10.100.0.100', 
		dimage="postgres:alpine")
	bib = net.addDocker('bib',
		ip='10.100.0.110', 
		environment={'POSTGRES_HOST':"10.100.0.100",
			'POSTGRES_DB':"bibpubdb",
                        'POSTGRES_USER':"bibpub",
                        'POSTGRES_PASSWORD':"@dm1n"},
		dcmd="python manage.py runserver 0.0.0.0:8000", 
		dimage="marcelopinto350/bibpub:3.1")
	sonar = net.addDocker('sonar', 
		ip='10.100.0.125', 
		volumes=["sonar_data:/opt/sonarqube/data",
			"sonar_extensions:/opt/sonarqube/extensions",
			"sonar_logs:/opt/sonarqube/logs"],
		dimage="sonarqube:lts-community")
	#d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
	info('*** Adicionando switches de rede\n')
	s1 = net.addSwitch('s1', failMode="standalone")
	#s2 = net.addSwitch('s2')
	info('*** Criando os links\n')
	net.addLink(pgbib, s1)
	net.addLink(bib, s1)
	net.addLink(sonar, s1)
	#net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
	#net.addLink(s1, bibpub)
	info('*** Iniciando a rede\n')
	net.build()
	net.addNAT().configDefault()
	s1.start([])
	info('*** Executando CLI\n')
	CLI(net)
	info('*** parando a rede')
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology()