# Generated by Django 4.2.7 on 2023-11-19 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0014_alter_autocompleteoption_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageopjournal',
            name='entry_is_valid',
            field=models.BooleanField(default=True, verbose_name='Запись валидна'),
        ),
    ]