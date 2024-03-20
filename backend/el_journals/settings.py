import ast
import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default=get_random_secret_key())

DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = ['127.0.0.1',
                 'localhost',
                 os.getenv('HOST_IP'),
                 os.getenv('HOST_NAME'),
                 # если пробрасываете порты в локальной сети то укажите их в след. строках
                 #'192.168.28.228',
                 ]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'widget_tweaks',
    'staff.apps.StaffConfig',
    'op_journal.apps.OpJournalConfig',
    'csvimport.app.CSVImportConf',
    'substation.apps.SubstationConfig',
    'powerline.apps.PowerlineConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = 'login'

ROOT_URLCONF = 'el_journals.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'substation.context_processors.substation_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'el_journals.wsgi.application'


# если дебаг включен, то разворачивается бд в sqlite, если не включен - postgres
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'django',
            'USER': 'django_user',
            'PASSWORD': 'django_password',
            'HOST': 'db',
            'PORT': 5432,
        }
    }

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

# если дебаг включен, то указываем размещение статики,
# если нет - точку сбора статики в корневой папке
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "staff.CustomUser"

# Далее настройки электронного журнала, все описания переменных в env-файле
NAME_MAX_LENGTH = int(os.getenv('NAME_MAX_LENGTH', default=64))
default_personal_position_str = os.getenv('DEFAULT_PERSONAL_POSITION', default="[('Системный администратор', 'Системный администратор'),]")
DEFAULT_PERSONAL_POSITION = ast.literal_eval(default_personal_position_str)
NUMBER_ENTRIES_OP_LOG_PAGE = int(os.getenv('NUMBER_ENTRIES_OP_LOG_PAGE', default=30))
TOTAL_VISIBLE_RECORDS_OPJ = int(os.getenv('TOTAL_VISIBLE_RECORDS_OPJ', default=1000))
REVERSE_EDITING_PERIOD = float(os.getenv('REVERSE_EDITING_PERIOD', default=5))
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', default=5))
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_FILE_SIZE * 1024 * 1024
MAX_ATTACHED_FILES = int(os.getenv('MAX_ATTACHED_FILES', default=5))
RETENTION_PERIOD_COMPLETED_RECORDS = int(os.getenv(
    'RETENTION_PERIOD_COMPLETED_RECORDS',
    default=10))
voltage_choices_str = os.getenv('VOLTAGE_CHOICES', default="(('220', '220'),)")
VOLTAGE_CHOICES = ast.literal_eval(voltage_choices_str)
SIGNAL_ON_REQUEST = int(os.getenv('SIGNAL_ON_REQUEST', default=48))
ISSUANCE_OF_CONFIRMATION = str(os.getenv('ISSUANCE_OF_CONFIRMATION', default='Не задано'))
PREPARATION_AND_ADMISSION = str(os.getenv('PREPARATION_AND_ADMISSION', default='Не задано'))
PRM_ONLY = str(os.getenv('PRM_ONLY', default='Не задано'))
ADMISSION_ONLY = str(os.getenv('ADMISSION_ONLY', default='Не задано'))
WITHOUT_TRIPPING = str(os.getenv('WITHOUT_TRIPPING', default='Не задано'))
AT_SUBSTATION = str(os.getenv('AT_SUBSTATION', default='Не задано'))
END_WORK = str(os.getenv('END_WORK', default='Не задано'))
SUBMIT_VL = str(os.getenv('SUBMIT_VL', default='Не задано'))
SUPER_ADMIN = os.getenv('SUPER_ADMIN', default=False)
