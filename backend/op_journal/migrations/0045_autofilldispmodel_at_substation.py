# Generated by Django 5.0.1 on 2024-02-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0044_autofilldispmodel_ending'),
    ]

    operations = [
        migrations.AddField(
            model_name='autofilldispmodel',
            name='at_substation',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Команда на работы на линейном оборудовании ПС"'),
        ),
    ]