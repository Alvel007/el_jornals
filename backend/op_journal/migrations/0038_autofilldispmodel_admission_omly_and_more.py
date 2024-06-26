# Generated by Django 5.0.1 on 2024-02-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0037_autofilldispmodel_prm_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='autofilldispmodel',
            name='admission_omly',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Команда на допуск"'),
        ),
        migrations.AlterField(
            model_name='autofilldispmodel',
            name='prm_only',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Команда на ПРМ"'),
        ),
        migrations.AlterField(
            model_name='autofilldispmodel',
            name='prm_tolerances',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Команда на ПРМиД на ВЛ"'),
        ),
    ]
