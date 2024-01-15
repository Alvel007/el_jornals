# Generated by Django 4.2.7 on 2023-12-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0029_mainpageopjournal_user_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpageopjournal',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='mainpageopjournal',
            name='user_position',
        ),
        migrations.AlterField(
            model_name='mainpageopjournal',
            name='user_signature',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись пользователя'),
        ),
    ]