# Generated by Django 5.0.1 on 2024-01-26 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0003_alter_mainpageopjournal_real_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageopjournal',
            name='user_signature',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись пользователя'),
        ),
    ]
