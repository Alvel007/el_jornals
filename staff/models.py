from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from el_journals.settings import NAME_MAX_LENGTH, DEFAULT_PERSONAL_POSITION
from substation.models import Substation, GroupSubstation


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ('employee_id',)
    ELECTRICAL_SAFETY_CHOICES = [
        ('III', 'III'),
        ('IV', 'IV'),
        ('V', 'V'),
    ]
    username = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name="Логин"
    )
    is_public = models.BooleanField(default=True,
                                    verbose_name='Отображать в списке персонала',)
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    middle_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Отчество'
    )
    birth_date = models.DateField(
        default='2000-01-01',
        verbose_name='Дата рождения',
        blank=True
    )
    position = models.CharField(
        max_length=120,
        default='',
        choices=DEFAULT_PERSONAL_POSITION,
        verbose_name="Должность",
        null=True
    )
    main_place_work = models.ForeignKey(Substation,
                                        on_delete=models.PROTECT,
                                        null=True, blank=True,
                                        verbose_name='Основное место работы',
                                        help_text = 'Указывается только для персонала, закрепленного за ПС по штатному расписания (необязательно для заполнения).')
    substation_group = models.ForeignKey(GroupSubstation,
                                        on_delete=models.PROTECT,
                                        null=True, blank=True,
                                        verbose_name='Группа подстанций',
                                        help_text = 'Указывается в какой группе ПС, ЦУС, ПМЭС, МЭС работает персонал.')
    employee_id = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Таб. номер',
        unique=True
    )
    electrical_safety_group = models.CharField(
        max_length=3,
        choices=ELECTRICAL_SAFETY_CHOICES,
        blank=True,
        verbose_name='Группа по ЭБ'
    )
    operational_staff = models.ManyToManyField(Substation,
                                               verbose_name='Оперативные права',
                                               related_name='operational_staff',
                                               blank=True)
    administrative_staff = models.ManyToManyField(Substation,
                                                  verbose_name='Административно-технические права',
                                                  default=None,
                                                  related_name='administrative_staff',
                                                  blank=True)
    admin_opj = models.ManyToManyField(Substation,
                                       verbose_name='Просмотр служебной информации оперативного журнала',
                                       default=None,
                                       related_name='admin_opj',
                                       blank=True)
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True,
                            editable=False)
    is_public = models.BooleanField(default=True,
                                    verbose_name='Отображать в списке персонала',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.username))
        super().save(*args, **kwargs)

    def __str__(self):
        first_initial = self.first_name[0] if self.first_name else ''
        middle_initial = self.middle_name[0] if self.middle_name else ''
        return f'{self.last_name} {first_initial}.{middle_initial}.'
