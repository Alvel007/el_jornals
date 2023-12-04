import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-hm%n!u0f==#$mddt(3p1%*hk#_8butdv80@gzsk3l419zr4p30'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

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
    'wkhtmltopdf',
    'widget_tweaks',
    'staff.apps.StaffConfig',
    'op_journal.apps.OpJournalConfig',
    'csvimport.app.CSVImportConf',
    'substation.apps.SubstationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'substation.middleware.AuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = 'login'

ROOT_URLCONF = 'el_journals.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'substation.context_processors.add_substations_to_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'el_journals.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'Europe/Samara'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "staff.CustomUser"

# Максимальная длина всех наименований
NAME_MAX_LENGTH = 64

# Тут перечислены все должности, которые допускается присваивать персоналу.
DEFAULT_PERSONAL_POSITION = [('Электромонтер по обслуживанию', 'Электромонтер по обслуживанию'),
                             ('Дежурный инженер', 'Дежурный инженер'),
                             ('Дежурный инженер 2 кат.', 'Дежурный инженер 2 кат.'),
                             ('Дежурный инженер 1 кат.', 'Дежурный инженер 1 кат.'),
                             ('Диспетчер ЦУС', 'Диспетчер ЦУС'),
                             ('Ведущий инженер гр. ПС', 'Ведущий инженер гр. ПС'),
                             ('Ведущий инженер по ОП гр. ПС', 'Ведущий инженер по ОП гр. ПС'),
                             ('Начальник ПС', 'Начальник ПС'),
                             ('Начальник гр. ПС', 'Начальник гр. ПС'),
                             ('Начальник ООР', 'Начальник ООР'),
                             ('Начальник ЦУС', 'Начальник ЦУС'),
                             ('АТП ПМЭС', 'АТП ПМЭС'),
                             ]

# Должности, которые могут быть назначены в управление группы ПС
# Название должно абсолютно соответствовать DEFAULT_PERSONAL_POSITION для последующего сопоставления в коде
HEAD_SUBSTATION_GROUP = ('Начальник гр. ПС',)

# Должности, которые могут быть назначены в управление ПС
HEAD_SUBSTATION = ('Начальник ПС',)

# Должности, которые могут быть назначены инженерами группы ПС
ENGINEER_SUBSTATION_GROUP = ('Ведущий инженер гр. ПС', 'Ведущий инженер по ОП гр. ПС',)

# Количество записей на одной странице оперативного журнала
NUMBER_ENTRIES_OP_LOG_PAGE = 30

# В течении какого периода допускается внесение записей в оперативный журнал задним числом (в часах)
REVERSE_EDITING_PERIOD = 22

WKHTMLTOPDF_CMD = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'

WKHTMLTOPDF_CMD_OPTIONS = {
 'quiet': True,
}
