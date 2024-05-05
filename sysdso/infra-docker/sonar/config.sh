#!/bin/sh
# Install Java
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk

# Download and extract SonarQube
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-8.9.1.44547.zip
unzip sonarqube-8.9.1.44547.zip
sudo mv sonarqube-8.9.1.44547 /opt/sonarqube

# Configure SonarQube
sudo nano /opt/sonarqube/conf/sonar.properties