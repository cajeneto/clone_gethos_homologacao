from pathlib import Path
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)  # Converte para booleano

ALLOWED_HOSTS = config('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF e CORS
CSRF_TRUSTED_ORIGINS = [
    'https://gethostecnologia.com.br',
    "https://teste2-gethos-crm.mtnwf6.easypanel.host",
    "https://teste2-hologacao-gethos-teste.mtnwf6.easypanel.host",
]

CORS_ALLOWED_ORIGINS = [
    "https://gethostecnologia.com.br",
    "https://teste2-gethos-crm.mtnwf6.easypanel.host",
    "https://teste2-hologacao-gethos-teste.mtnwf6.easypanel.host",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gethos_home.apps.GethosHomeConfig",
    "channels",
    "rest_framework",
    "cadastros",
    "processos",
    "notificacoes",
    "perfil",
    "relatorios",
    "integration_api_zwa",
    "landing_page_gethos",
    "configuracoes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configurações de e-mail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Token do GitHub (removido do código, agora no .env)
TOKEN_GITHUB = config('TOKEN_GITHUB')

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
ASGI_APPLICATION = "gethosapp.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}




# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # "NAME": "teste_gethos_db",
        "NAME": "gethosapp_db",
        # "USER": "postgres",
        "USER": "gethosapp_db_teste",
        # "USER": "gethosapp_db_teste",
        "PASSWORD": "gethosappsenha",
        "HOST": "teste2_teste_gethos_db",
        # "HOST": "127.0.0.1",
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "processos" / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = 'home'
LOGIN_REDIRECT_URL = 'dashboard_auth'
LOGOUT_REDIRECT_URL = 'home'

# Celery
CELERY_TIMEZONE = 'UTC'
# CELERY_BROKER_URL = "redis://default:redis://127.0.0.1:6379/1:6379/0"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_BACKEND = "redis://default:redis://127.0.0.1:6379/1:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Simplesvet
# SIMPLESVET_EMAIL = config('SIMPLESVET_EMAIL')
# SIMPLESVET_PASSWORD = config('SIMPLESVET_PASSWORD')