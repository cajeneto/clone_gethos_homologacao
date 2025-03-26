from pathlib import Path
import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mv1tfce_$46b(po8ij_$69y4)!paib(3o-ato+)9oo-2(x9u)a"

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #variáveis de ambientes

# ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOST', '').split(',')

ALLOWED_HOSTS = ["*"]








#ALLOWED_HOSTS = ['167.172.206.194', 'gethostecnologia.com.br', 'localhost', '127.0.0.1']


# inserido CSRF confiável data 26/11/2024

# CSRF_TRUSTED_ORIGINS = [
#     'https://gethostecnologia.com.br',
#     'http://gethostecnologia.com.br',
# ]


CORS_ALLOWED_ORIGINS = [
    "https://gethostecnologia.com.br",
    # "http://127.0.0.1:3000",  # Outro possível domínio local
    
]



# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "gethos_home",
    "cadastros",
    "processos",
    "notificacoes",
    "perfil",
    "relatorios",
    "integration_api_zwa",
    "landing_page_gethos",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'corsheaders.middleware.CorsMiddleware',
]


TOKEN_GITHUB = "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"

AUTH_USER_MODEL = 'gethos_home.Usuario'

ROOT_URLCONF = "gethosapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "gethos_home" / "templates",
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,  
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gethosapp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "gethosapp_db",
	"USER": "postgres",
	"PASSWORD": "gethosappsenha",
	"HOST": "127.0.0.1",
	"PORT": "5432",
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "processos" / "static",
    
]
#STATIC_ROOT = BASE_DIR / "staticfiles"



#MEDIA_URL = '/staticfiles/'
#MEDIA_ROOT = '/webapps/gethosapp/projetoGethos/media/'
#MEDIA_ROOT = 'staticfiles/'





# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # URL para redirecionar após o login
# LOGIN_REDIRECT_URL = 'dashboard.auth'

# # URL para redirecionar ao fazer logout
# LOGOUT_REDIRECT_URL = 'home'

LOGIN_URL = 'home'
LOGIN_REDIRECT_URL = 'dashboard_auth'
LOGOUT_REDIRECT_URL = 'home'


# Timezone
CELERY_TIMEZONE = 'UTC'

# Aceitar apenas formatos JSON
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Redis precisa estar rodando
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"


# Backend opcional para armazenar os resultados das tarefas
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'




SIMPLESVET_EMAIL= "netocajeh@gmail.com"
SIMPLESVET_PASSWORD= "Neto03@@"



