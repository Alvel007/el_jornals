# Generated by Django 4.2.7 on 2023-12-12 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substation', '0003_alter_substation_slug'),
        ('staff', '0010_alter_customuser_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='admin_opj',
            field=models.ManyToManyField(blank=True, default=None, related_name='admin_opj', to='substation.substation', verbose_name='Просмотр служебной информации'),
        ),
    ]
