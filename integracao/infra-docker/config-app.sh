#!/bin/sh

# verificando e criando a imagem do bibpub caso não exista
cd ~
if [ ! -d bibpub-imd ]; then
   git clone https://github.com/MarceloPinto350/bibpub.git
fi
# subindo o container
cd bibpub
docker-compose up -d
# disponivel em http://localhost:8000

# verificando e criando a imagem do DVWA caso não exista
cd ~
if [ ! -d DVWA ]; then
   git clone https://github.com/digininja/DVWA.git 
fi
# subindo o container
cd DVWA
# ajustar o compose.yml antes de subir
# alterar pull_policy=always para pull_policy=build
# aLterar a url para 0.0.0.0 ao invés de loalhost
docker-compose up -d
# disponivel em http://localhost:4280



#!/usr/bin/python
"""
Este é um script para subir o sonarqube no containernet, com as configurações necessárias
"""
from containernet.cli import CLI
from containernet.link import TCLink
from containernet.net import Containernet
from mininet.node import Controller
from mininet.log import info, setLogLevel

setLogLevel('info')

net = Containernet(controller=Controller)

info('*** Adicinando um controlador\n')
net.addController('c0')
info('*** Adicionando um container para o SonarQube\n')
d1 = net.addDocker('postgres_bib', volumes=["postgres_data:/var/lib/postgresql/data"], ip='10.0.0.100', dimage="postgres:alpine")
d2 = 
d3 = net.addDocker('sonar', ip='10.0.0.125', dimage="sonarqube:lts-community")
#d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
info('*** Adcoinando um switch de rede\n')
s1 = net.addSwitch('s1')
#s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(d1, s1)
#net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
#net.addLink(s2, d2)
info('*** Starting network\n')
net.start()
#info('*** Testing connectivity\n')
#net.ping([d1, d2])
info('*** Running CLI\n')
