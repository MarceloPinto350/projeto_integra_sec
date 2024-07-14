FROM owasp/burp-suite-community

RUN apt-get update && apt-get install -y ca-certificates \
    curl gnupg2 lsb-release iproute2 net-tools

# Instalar o Java 11
RUN apt-get install -y openjdk-11-jdk

# Definir a variável de ambiente JAVA_HOME para o Java 11
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

# Copiar o arquivo de licença do Burp Suite para o container
COPY burp-suite-community_2023.1_linux.tar.gz /opt/burp-suite/

# Extrai o arquivo de licença
RUN tar -xf /opt/burp-suite/burp-suite-community_2023.1_linux.tar.gz -C /opt/burp-suite/

# Define a variável de ambiente BURP_LICENSE_FILE para o arquivo de licença
ENV BURP_LICENSE_FILE /opt/burp-suite/burp-suite-community_2023.1_linux/license.lic

# Define a porta de acesso para o Burp Suite
EXPOSE 8080

# Comando para executar o Burp Suite
CMD ["/opt/burp-suite/bin/java", "-jar", "/opt/burp-suite/burp-suite-community_2023.1_linux/burpsuite.jar"]


# compose.yml
# burp suite - para fazer verificação de segurança (DAST)
#burp:
#   image: bkimminich/juice-shop
#   container_name: juice-shop-mandso
#   ports:
#     - "3000:3000"
#   environment:
#     NODE_ENV: "juice-shop"
#   depends_on:
#     - postgres
#   links:
#     - postgres

