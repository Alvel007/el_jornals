# Generated by Django 5.0.1 on 2024-02-05 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0023_alter_selecteddata_induced_voltage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecteddata',
            name='CUS_dispatcher',
            field=models.TextField(max_length=100, verbose_name='Экспл.ведение'),
        ),
    ]
