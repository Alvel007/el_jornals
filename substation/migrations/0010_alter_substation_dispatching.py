# Generated by Django 5.0.1 on 2024-01-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substation', '0009_substation_dispatching'),
    ]

    operations = [
        migrations.AlterField(
            model_name='substation',
            name='dispatching',
            field=models.ManyToManyField(blank=True, to='substation.substation', verbose_name='Связанные записи'),
        ),
    ]
