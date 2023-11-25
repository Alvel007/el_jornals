from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from el_journals.settings import NAME_MAX_LENGTH, DEFAULT_PERSONAL_POSITION



class Substation(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название ПС')
    address = models.CharField(max_length=128,
                               verbose_name='Адрес')
    substation_boss = models.ForeignKey('staff.CustomUser',
                                        on_delete=models.PROTECT,
                                        null=True, blank=True,
                                        verbose_name='Начальник ПС')
    group_substation = models.ForeignKey('GroupSubstation',
                                         on_delete=models.PROTECT,
                                         null=True, blank=True,
                                         verbose_name='Группа подстанций')
    slug = models.SlugField(verbose_name='Слаг',
                            unique=True,
                            editable=False)

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
                            verbose_name='Название группы ПС',
                            unique=True)
    group_boss = models.CharField(max_length=NAME_MAX_LENGTH,
                                  null=True, blank=True,
                                  verbose_name=[item[1] for item in DEFAULT_PERSONAL_POSITION if item[0] == 'Начальник гр. ПС'][0])
    group_engineer = models.CharField(max_length=NAME_MAX_LENGTH,
                                      null=True,
                                      blank=True,
                                      verbose_name=[item[1] for item in DEFAULT_PERSONAL_POSITION if item[0] == 'Ведущий инженер гр. ПС'][0])
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
