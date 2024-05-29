FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /appseg

# Atualizando a instalando as dependências do SO
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y linux-headers net-tools apt-transport-https \
   ca-certificates curl openssh-server openssl postgresql-client \
   iproute2 net-tools

# Instalando asconfigurações para o Python
RUN pip install -U pip setuptools 

# Copiando os arquivos da aplicação e dependências para o container
ADD ../../../../. .

# Instalando as dependências do Python
RUN pip install -r requirements.txt

# Espendo o Django service na máquina
EXPOSE 8000