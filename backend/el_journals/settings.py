import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-hm%n!u0f==#$mddt(3p1%*hk#_8butdv80@gzsk3l419zr4p30'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.2.12',]
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
                'substation.context_processors.substation_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'el_journals.wsgi.application'

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

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

STATIC_URL = '/backend_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/backend_media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://192.168.2.12',
    ]

AUTH_USER_MODEL = "staff.CustomUser"

# Максимальная длина всех наименований
NAME_MAX_LENGTH = 64

# Тут перечислены все должности, которые допускается присваивать персоналу.
DEFAULT_PERSONAL_POSITION = [('Электромонтер по обслуживанию', 'Электромонтер по обслуживанию'),
                             ('Дежурный инженер', 'Дежурный инженер'),
                             ('Дежурный инженер 2 кат.', 'Дежурный инженер 2 кат.'),
                             ('Дежурный инженер 1 кат.', 'Дежурный инженер 1 кат.'),
                             ('Диспетчер', 'Диспетчер'),
                             ('Ведущий инженер', 'Ведущий инженер'),
                             ('Ведущий инженер по ОП', 'Ведущий инженер по ОП'),
                             ('Начальник', 'Начальник'),
                             ('Начальник ООР', 'Начальник ООР'),
                             ('АТП', 'АТП'),
                             ('Зам. гл. инженера', 'Зам. гл. инженера'),
                             ('Главный инженер', 'Главный инженер'),
                             ('Системный администратор', 'Системный администратор'),
                             ]

# Должности, которые могут быть назначены в управление группы ПС
# Название должно абсолютно соответствовать DEFAULT_PERSONAL_POSITION для последующего сопоставления в коде
HEAD_SUBSTATION_GROUP = ('Начальник',)

# Количество записей на одной странице оперативного журнала
NUMBER_ENTRIES_OP_LOG_PAGE = 30

# Количество записей опер. журнала, доступных для просмотра рядовым пользователем
TOTAL_VISIBLE_RECORDS_OPJ = 1000

# В течении какого периода допускается внесение записей в оперативный журнал задним числом (в часах).
# Рекомендуется НЕ ставить менее 0,25 часа, чтобы персонал успевал заполнять содержание записи, не обновляя поле "Время выполнения действия"
# дробные значения указывать через точку (например 0.25)
REVERSE_EDITING_PERIOD = 5

# Размер максимального загружаемого файла в МБ
# дробные значения указывать через точку (например 0.25)
MAX_FILE_SIZE = 5
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_FILE_SIZE * 1024 * 1024

# Допустимое количество файлов, которое можно прикрепить в одной записи.
MAX_ATTACHED_FILES = 5

# Скольео дней, после ввода в работу/окончания работ, отображается запись в разделе "Законченные работы"
# Только целые числа
RETENTION_PERIOD_COMPLETED_RECORDS = 10


# Классы напряжения ВЛ диспетчерских пунктов
VOLTAGE_CHOICES = (
        ('220', '220'),
        ('500', '500'),
    )

# За сколько часов до предстоящего ввода в работу оборудования, запись начинает подкрашиваться желтым цветом.
SIGNAL_ON_REQUEST = 48

# Типовая запись в ОЖ диспетчера по приему ВЛ от диспетчера
ISSUANCE_OF_CONFIRMATION = ('{0} {1} {2}\n'
                           'Операции по отключению, заземлению, переключениям во вторичных '
                           'цепях выполнены. {3} отключена '
                           'и заземлена в сторону линии на {4} '
                           '. На приводах линейных '
                           'разъединителей {4} '
                           'вывешены '
                           'плакаты «Не включать! Работа на линии». На '
                           ' {4} приняты меры, препятствующие '
                           'подаче напряжения на {3} вследствие '
                           'ошибочного или самопроизвольного включения коммутационных аппаратов.\n'
                           'После выполнения иных технических мероприятий, предусмотренных нарядами-'
                           'допусками, организуйте выдачу разрешений на подготовку рабочих мест и '
                           'допуск бригад для безопасного производства работ на {3}.\n'
                           'Работы закончить до {5}, с аварийной готовностью {6}.')

# Типовая запись в ОЖ диспетчера по ПРМиД бригады на ВЛ
PREPARATION_AND_ADMISSION = ('Допускающему {0} {1} {2}\n'
                             'Операции по отключению, заземлению, переключениям во '
                             'вторичных цепях выполнены. {3} '
                             'отключена и заземлена в сторону линии на {4}. '
                             'На приводах линейных разъединителей {3} на '
                             '{4} вывешены плакаты «Не включать! Работа на линии». '
                             'На {4} приняты меры, препятствующие '
                             'подаче напряжения на {3} вследствие ошибочного или самопроизвольного '
                             'включения коммутационных аппаратов.\n'
                             'Вам разрешается по наряду-допуску №!!!НОМЕР НАРЯДА!!! подготовка рабочего места и допуск '
                             'бригады для выполнения следующих работ: "***НАИМЕНОВАНИЕ РАБОТ ПО ЗАЯВКЕ***".\n'
                             'Работы закончить до {5}, с аварийной готовностью {6}.')

PRM_ONLY = ('Допускающему {0} {1} {2}\n'
            'Операции по отключению, заземлению, переключениям во вторичных цепях выполнены. '
            '{3} отключена и заземлена в сторону линии на {4}. '
            'На приводах линейных разъединителей {3} на {4} вывешены плакаты «Не включать! '
            'Работа на линии». На {4} приняты меры, препятствующие подаче напряжения '
            'на {3} вследствие ошибочного или самопроизвольного включения коммутационных аппаратов.\n'
            'Вам разрешается по наряду-допуску ***НОМЕР НАРЯДА*** подготовка рабочего места для '
            'выполнения следующих работ: "***НАИМЕНОВАНИЕ РАБОТ ПО ЗАЯВКЕ***".')

ADMISSION_ONLY = ('Допускающему {0} {1} {2}\n'
                  '{3}.\n'
                  'Вам разрешается по наряду-допуску №***НОМЕР НАРЯДА*** допуск бригады '
                  'для выполнения следующих работ: "***НАИМЕНОВАНИЕ РАБОТ ПО ЗАЯВКЕ***".\n'
                  'Работы закончить до {4}, с аварийной готовностью {5}.')

WITHOUT_TRIPPING = ('Допускающему {0} {1} {2}\n'
                    '{3} находится в работе, под напряжением. '
                    'На {4} вывешены запрещающие плакаты «Работа под напряжением, '
                    'повторно не включать!» на ключах дистанционного управления '
                    'выключателей ВЛ. АПВ {3} выведено.\n'
                    'Вам разрешается по ***НАРЯДУ-ДОПУСКУ/РАСПОРЯЖЕНИЮ № НОМЕР*** допуск бригады '
                    'для выполнения следующих работ: "***НАИМЕНОВАНИЕ РАБОТ ПО ЗАЯВКЕ***".\n'
                    'Работы выполнять без приближения к токоведущим частям на расстояние менее допустимого.\n'
                    'Работы закончить до {5}, с аварийной готовностью {6}.')

AT_SUBSTATION = ('{0}. Допускающему !!!ФИО ДОПУСКАЮЩЕГО!!!\n'
                 'Операции по отключению, заземлению, переключениям во вторичных цепях выполнены. '
                 '{1} отключена и заземлена в сторону линии на {2}. На приводах линейных разъединителей '
                 '{1} на {2} вывешены плакаты «Не включать! Работа на линии». '
                 'На {2} приняты меры, препятствующие подаче напряжения на {1} '
                 'вследствие ошибочного или самопроизвольного включения коммутационных аппаратов.\n'
                 'Вам разрешается по наряду-допуску №***НОМЕР НАРЯДА*** подготовка рабочего '
                 'места и допуск бригады для выполнения следующих работ: "***НАИМЕНОВАНИЕ РАБОТ ПО ЗАЯВКЕ***".\n'
                 'Работы закончить до {3}, с аварийной готовностью {4}.')

END_WORK = ('Работы по ***НАРЯДУ-ДОПУСКУ/РАСПОРЯЖЕНИЮ №НОМЕР*** '
            'на {0} по "***НАИМЕНОВАНИЕ РАБОТ ПО ЗАЯВКЕ***" полностью закончены. '
            'Бригада с рабочего места выведена, механизмы удалены. '
            'Переносные заземления, установленные бригадой в процессе работ, сняты.\n'
            'Наряд №***НОМЕР*** закрыт.\n'
            '{0} можно вводить в работу.')

SUBMIT_VL = ('{0} {1} {2}\n'
             'Работы на {3}, в том числе на оборудовании подключенном к ВЛ '
             'без коммутационных аппаратов, полностью закончены. Бригады с рабочего '
             'места выведены, механизмы удалены. Переносные заземления, установленные '
             'бригадой в процессе работ, сняты.\n{3} можно вводить в работу.')

# Разрешить редактирование записей и комментариев из админ-панели
SUPER_ADMIN = False
