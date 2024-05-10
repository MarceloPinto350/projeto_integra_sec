FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalando as dependências do SO
RUN apt-get update && apt-get upgrade -y && apt-get install -y net-tools \
   apt-transport-https ca-certificates curl openssh-server openssl \
   postgresql-client 

# Instalando as configurações para o Python
RUN pip install -U pip setuptools 

# Copiando o código da aplicação para o container
ADD . .

# Instalando as dependências do Python
RUN pip install -r requirements.txt

# Executando a aplicação mesmo sem ter feito migration do banco de dados
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Expondo o Django service na máquina
EXPOSE 8000
