# Generated by Django 5.0.1 on 2024-02-11 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0036_autofilldispmodel_admitting_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='autofilldispmodel',
            name='prm_only',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='Текст "Команда на допуск (без ПРМиД)"'),
        ),
    ]