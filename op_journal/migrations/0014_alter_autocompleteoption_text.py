# Generated by Django 4.2.7 on 2023-11-18 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0013_autocompleteoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autocompleteoption',
            name='text',
            field=models.CharField(max_length=4096, verbose_name='Текст автозаполнения'),
        ),
    ]