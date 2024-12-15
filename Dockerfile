FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /appseg
WORKDIR /appseg

# Instalando as dependências do SO
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y net-tools apt-transport-https ca-certificates curl openssh-server openssl postgresql-client iproute2 ethtool

# Instalando asconfigurações para o Python
RUN pip install -U pip setuptools 

# Copiando o arquivo de dependências para o container
COPY requirements.txt requirements.txt

# Instalando as dependências do Python
RUN pip install -r requirements.txt 

# Copiando o arquivo de configuração do Django para o container
COPY . .

# Acrescentando as variáveis de ambiente
ENV POSTGRES_HOST '10.100.0.150'
ENV POSTGRES_PORT '5432'
ENV POSTGRES_DB 'appseg'
ENV POSTGRES_USER 'postgres'
ENV POSTGRES_PASSWORD 'postgres'
ENV URL_API 'http://10.21.220.150:8000/api'

# Expondo o Django service na máquina
EXPOSE 8000

# Executando a aplicação quando o container inicia
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

