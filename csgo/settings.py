from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get('DEBUG_VALUE', 0))
ALLOWED_HOSTS = ['localhost','127.0.0.1']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

AUTH_USER_MODEL = 'steam.User'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
    'django.contrib.auth.backends.ModelBackend',
)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # my apps
    'steam',
    'stats.apps.StatsConfig',
    'store.apps.StoreConfig',

    #Thirdparty
    'crispy_forms',
    'social_django',
    'django_filters',
    'debug_toolbar',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'csgo.urls'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'csgo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_DEFAULT_NAME'),  
        'USER': os.environ.get('DB_DEFAULT_USER'),  
        'PASSWORD': os.environ.get('DB_DEFAULT_PASS'),  
        'HOST': os.environ.get('DB_DEFAULT_HOST'),  
        'PORT': os.environ.get('DB_DEFAULT_PORT'),  
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },'retake':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_RETAKE_NAME'),  
        'USER':os.environ.get('DB_RETAKE_USER'),  
        'PASSWORD':os.environ.get('DB_RETAKE_PASS'),  
        'HOST':os.environ.get('DB_RETAKE_HOST'),  
        'PORT':os.environ.get('DB_RETAKE_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },'warmup':{
                'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_WARMUP_NAME'),  
        'USER':os.environ.get('DB_WARMUP_USER'),  
        'PASSWORD':os.environ.get('DB_WARMUP_PASS'),  
        'HOST':os.environ.get('DB_WARMUP_HOST'),  
        'PORT':os.environ.get('DB_WARMUP_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },'pug':{
                'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_PUG_NAME'),  
        'USER':os.environ.get('DB_PUG_USER'),  
        'PASSWORD':os.environ.get('DB_PUG_PASS'),  
        'HOST':os.environ.get('DB_PUG_HOST'),  
        'PORT':os.environ.get('DB_PUG_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4'
        }

    }}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static_root')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR,'uploads')

LOGIN_REDIRECT_URL = 'stats:index'

SOCIAL_AUTH_STEAM_API_KEY = os.environ.get('STEAM_API_KEY')
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = ('social_core.backends.steam.SteamOpenId',)

STEAM_WEB_API_KEY = os.environ.get('STEAM_API_KEY')
CRISPY_TEMPLATE_PACK = 'bootstrap4' 

KHALTI_API_PUBLIC_KEY = os.environ.get('KHALTI_API_PUBLIC_KEY')
KHALTI_API_SECRET_KEY = os.environ.get('KHALTI_API_SECRET_KEY')

KHALTI_VERIFICATION_URL = 'https://khalti.com/api/v2/payment/verify/'

REPORT_DISCORD_WEBHOOK_URL = os.environ.get('REPORT_DISCORD_WEBHOOK_URL')
APPEAL_DISCORD_WEBHOOK_URL = os.environ.get('APPEAL_DISCORD_WEBHOOK_URL')
CONTACT_DISCORD_WEBHOOK_URL = os.environ.get('CONTACT_DISCORD_WEBHOOK_URL')

ADMINS = [(os.environ.get('ADMIN_ONE_NAME'),os.environ.get('ADMIN_ONE_EMAIL'),)]
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')


# For Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]