from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from el_journals.settings import NAME_MAX_LENGTH, VOLTAGE_CHOICES
from substation.models import Substation
from unidecode import unidecode


class DispatchCompanies(models.Model):
    full_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Полное наименование организации диспетчерского центра',
        unique=True,
        blank=False,)
    abbreviated_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Сокращенное наименование',
        unique=True,
        blank=False,)
    abbreviated_name_rp = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='',
        unique=True, blank=False,
        help_text='Сокращенное наименование ДЦ в родительском падеже')

    class Meta:
        verbose_name = 'Диспетчерский центр'
        verbose_name_plural = 'Диспетчерские центры'

    def __str__(self):
        return self.abbreviated_name


class ThirdPartyDispatchers(models.Model):
    disp_post = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Должность персонала стороннего ДЦ',
        null=True,
        blank=False,)
    disp_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Фамилия И.О.',
        null=True,
        blank=False,)
    disp_center = models.ForeignKey(
        DispatchCompanies,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='disp_center',
        verbose_name='Диспетчерский центр')

    class Meta:
        verbose_name = 'Сторонний диспетчер'
        verbose_name_plural = 'Сторонние диспетчера'

    def __str__(self):
        return self.disp_name

    def clean(self):
        # Проверка на уникальность поля disp_name
        existing_dispatchers = ThirdPartyDispatchers.objects.filter(
            disp_name=self.disp_name)
        if self.pk:
            existing_dispatchers = existing_dispatchers.exclude(pk=self.pk)
        if existing_dispatchers.exists():
            raise ValidationError('Диспетчер с такими ФИО уже существует. '
                                  'Укажите инициалы, состояние из 2ух букв!')


class PowerLine(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Наименование ЛЭП',
        unique=True,
        help_text='Диспетчерское наименование ВЛ',)
    voltage = models.CharField(
        max_length=3,
        verbose_name='Напряжение ВЛ',
        choices=VOLTAGE_CHOICES,
        null=False,
        blank=False,
        help_text='Класс напряжения',)
    disp_manage = models.ForeignKey(
        DispatchCompanies,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='В управлении ДЦ',
        related_name='disp_manage',)
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        editable=False,)
    ending = models.ManyToManyField(
        Substation,
        blank=True,
        verbose_name='ВЛ заходит на следующие ПС',
        limit_choices_to={'dispatch_point': False},
        help_text='Обязательное поле',
        related_name='powerline_endings',)
    third_party_object_1 = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Сторонний объект 1',
        null=True,
        blank=True,
        help_text=('Если ВЛ подключена к объектам третьих лиц, укажите ДН '
                   'этого объекта (необязательное поле). Объекты генерации '
                   'указывать в родительском падеже.'),)
    third_party_object_2 = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Сторонний объект 2',
        null=True,
        blank=True,
        help_text=('Если ВЛ подключена к объектам третьих лиц, укажите ДН '
                   'этого объекта (необязательное поле). Объекты генерации '
                   'указывать в родительском падеже.'),)
    third_party_object_3 = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Сторонний объект 3',
        null=True,
        blank=True,
        help_text=('Если ВЛ подключена к объектам третьих лиц, укажите ДН '
                   'этого объекта (необязательное поле). Объекты генерации '
                   'указывать в родительском падеже.'),)
    induced_voltage = models.BooleanField(
        verbose_name='Наличие наведенного напряжения на ВЛ',
        default=False,
        null=False,
        blank=False,)
    for_CUS_dispatcher = models.ManyToManyField(
        Substation,
        blank=True,
        verbose_name='Интересна диспетчеру',
        limit_choices_to={'dispatch_point': True},
        help_text=('В эксплуатационной ответственности какого '
                   'диспетчера находится указанная ВЛ?'),
        related_name='dispatcher_interests',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Линия электропередач'
        verbose_name_plural = 'Линии электропередач'

    def __str__(self):
        return self.name


class AdmittingStaff(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Фамилия И.О.',
        unique=True,
        blank=False,
        help_text='Фамилия И.О. В дательном падеже (кому?)')
    position = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Должность',
        null=True,
        blank=True,
        help_text='Должность допускающего. В дательном падеже (кому?)')
    organization = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='От организации',
        null=True, blank=True,
        help_text=('Организация, где работает допускающий. '
                   'В родительном падеже (нет чего?)'))
    for_CUS_dispatcher = models.ManyToManyField(
        Substation,
        blank=True,
        verbose_name='Для диспетчера ЦУС',
        limit_choices_to={'dispatch_point': True},
        help_text=('Какому диспетчеру будет доступен этот '
                   'допускающий для заполнения автоформы'),
        related_name='dispatcher_admit')

    class Meta:
        verbose_name = 'Допускающий'
        verbose_name_plural = 'Допускающий персонал'

    def __str__(self):
        return self.name

    def clean(self):
        # Проверка на уникальность поля disp_name
        existing_admitting = AdmittingStaff.objects.filter(name=self.name)
        if self.pk:
            existing_admitting = existing_admitting.exclude(pk=self.pk)
        if existing_admitting.exists():
            raise ValidationError('Допускающий с такими ФИО уже существует. '
                                  'Укажите инициалы, состояние из 2ух букв!')
