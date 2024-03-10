from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from el_journals.settings import NAME_MAX_LENGTH


class Substation(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название ПС',
                            unique=True,
                            help_text='Указываются только подстанции предприятия')
    address = models.CharField(max_length=128,
                               verbose_name='Адрес')
    group_substation = models.ForeignKey('GroupSubstation',
                                         on_delete=models.PROTECT,
                                         null=True, blank=True,
                                         verbose_name='Группа подстанций',
                                         help_text='Прописываются только существующие группы ПС')
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True,
                            editable=False)
    dispatch_point = models.BooleanField(verbose_name='Является диспетчерским пунктом',
                                         default=False)
    dispatcher_for = models.ManyToManyField('self',
                                            blank=True,
                                            verbose_name='Диспетчер для ПС:',
                                            help_text='Выберите объекты для диспетчеризации этого ДП',)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подстанция'
        verbose_name_plural = 'Подстанции'

    def __str__(self):
        return self.name


class GroupSubstation(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название группы ПС, ЦУС, ПМЭС или МЭС',
                            unique=True,
                            help_text='Указываются группы ПС, ЦУС, предприятия, а также МЭС')
    name_rp = models.CharField(max_length=NAME_MAX_LENGTH,
                               verbose_name='Название СП в родительском падеже',
                               null=True, blank=True,
                               help_text='Название группы этого же структурного подразделения в родительском падеже')
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True,
                            editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Группа подстанций'
        verbose_name_plural = 'Группы подстанций'

    def __str__(self):
        return self.name
