from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from el_journals.settings import NAME_MAX_LENGTH, VOLTAGE_CHOICES, PMES_CHOICES
from substation.models import Substation


class PowerLine(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Наименование ЛЭП',
                            unique=True,
                            help_text='Диспетчерское наименование ВЛ')
    voltage = models.CharField(max_length=3,
                               verbose_name='Напряжение ВЛ',
                               choices=VOLTAGE_CHOICES,
                               null=False, blank=False,
                               help_text='Класс напряжения')
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True,
                            editable=False)
    ending_1 = models.ForeignKey(Substation,
                                 on_delete=models.PROTECT,
                                 null=False, blank=False,
                                 verbose_name='Заходит на ПС 1',
                                 related_name='powerline_ending_1',
                                 limit_choices_to={'dispatch_point': False})
    ending_2 = models.ForeignKey(Substation,
                                 on_delete=models.PROTECT,
                                 null=False, blank=False,
                                 verbose_name='Заходит на ПС 2',
                                 related_name='powerline_ending_2',
                                 limit_choices_to={'dispatch_point': False})
    ending_3 = models.ForeignKey(Substation,
                                 on_delete=models.PROTECT,
                                 null=True, blank=True,
                                 verbose_name='Заходит на ПС 3',
                                 related_name='powerline_ending_3',
                                 limit_choices_to={'dispatch_point': False},
                                 help_text='Указывается только если на ВЛ есть одна отпайка')
    ending_4 = models.ForeignKey(Substation,
                                 on_delete=models.PROTECT,
                                 null=True, blank=True,
                                 verbose_name='Заходит на ПС 4',
                                 related_name='powerline_ending_4',
                                 limit_choices_to={'dispatch_point': False},
                                 help_text='Указывается только если на ВЛ есть вторая отпайка')
    Induced_voltage = models.BooleanField(verbose_name='Наличие наведенного напряжения на ВЛ',
                                          default=False,
                                          null=False, blank=False)

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
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Фамилия И.О.',
                            unique=True, blank=False,)
    position = models.CharField(max_length=NAME_MAX_LENGTH,
                                verbose_name='Должность',
                                unique=False, blank=False,
                                help_text='Указать должность, как она будет отображаться в оперативном журнале')
    oganization = models.CharField(max_length=20,
                                   verbose_name='Выберете предприятие',
                                   choices=PMES_CHOICES,
                                   null=True, blank=True,
                                   help_text='Класс напряжения')
    
    class Meta:
        verbose_name = 'Допускающий'
        verbose_name_plural = 'Допускающий персонал'
    
class ManufacturerStaff(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Фамилия И.О.',
                            unique=True, blank=False,)
    position = models.CharField(max_length=NAME_MAX_LENGTH,
                                verbose_name='Должность',
                                unique=False, blank=False,
                                help_text='Указать должность, как она будет отображаться в оперативном журнале')
    oganization = models.CharField(max_length=NAME_MAX_LENGTH,
                                verbose_name='Организация',
                                unique=True,)
    
    class Meta:
        verbose_name = 'Производитель работ'
        verbose_name_plural = 'Производители работ'
    