"""
Django settings for integracao project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/

<Token ADMIN: d869109dc87e9803567c13eda1820cffa6c2d00c>
<Token MMPINTO: f0ee4a32f947f00cc06202ee306b5524fe1f3590>

"""

from pathlib import Path
import os

from corsheaders.defaults import default_headers    # para permitir acesso de qualquer origem
#import environ # para carregar variáveis de ambiente precisa instalar o pacote pip install django-environ
#env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# ler o arquivo .env local para carregar as variáveis de ambiente
#environ.Env.read_env()
#DEBUG = env('DEBUG')
#SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^q&m4yv8-&yrz&)e(mh=&2r3+(_c3091y%0p6#p7dprs3a6(n3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["192.168.0.22","10.100.0.155","192.168.0.4","localhost","127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # configurações para o django-rest-framework
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken', # para permitir autenticação via tokentokn
    'corsheaders', # para permitir acesso de qualquer origem
    # configurações para a aplicação de segurança
    'seguranca', 
    #'sonar_data',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'corsheaders.middleware.CorsMiddleware', # para permitir acesso de qualquer origem
    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

CORS_ALLOWED_ORIGINS = [
    # permitir configurar o acesso de qualquer origem
    "http://localhost:8000",
    "http://192.168.0.22:8000",
    "http://10.100.0.155:8000",
    "http://10.100.0.155:8000",
    "http://192.168.0.4:8000",
    
]

CORS_ALLOWED_HEADERS = list(default_headers) + [
    'contenttype',
]

ROOT_URLCONF = 'integracao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'integracao.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '192.168.0.13',  # os.getenv('POSTGRES_HOST'),
        'NAME': 'appseg',       #os.getenv('POSTGRES_DB'),
        'USER': 'postgres',     #os.getenv('POSTGRES_USER'),
        'PASSWORD': 'postgres', #os.getenv('POSTGRES_PASSWORD'),
        'PORT': '32771'         #os.getenv('POSTGRES_PORT')
    }    
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIT_ROOT = os.path.join (BASE_DIR, 'staticfiles')
MEDIA_URL = 'midia/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'midia')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Rest Framework (DRF) settings
REST_FRAMEWORK = {    

    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.SessionAuthentication', # para autenticação via sessão
        'rest_framework.authentication.TokenAuthentication', # para autenticação via token
    ],  
    # CONFIGURAÇÕES DE SEGURANÇA DE NÍVEL GLOBAL
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticatedOrReadOnly',    # para permitir leitura sem autenticação
        #'rest_framework.permissions.IsAuthenticated',              # para permitir autenticação em todas as rotas
        'rest_framework.permissions.AllowAny',                     # para permitir acesso sem autenticação em todas as rotas
    ],
    # definindo a paginação padrão para 2 registros por página
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    # configurando o limite global de requisições por segundo para a API
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    "DEFAULT_THROTTLE_RATES": { # Pode ser limitado por dia, segundo, hora etc e também por IP, usuário ou grupo)
        'anon': '6/minute',     # 6 requisições por minuto para usuários anônimos
        'user': '100/minute',   # 100 requisições por minuto para usuários autenticados
    }
}