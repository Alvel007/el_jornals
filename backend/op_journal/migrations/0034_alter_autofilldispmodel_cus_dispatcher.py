# Generated by Django 5.0.1 on 2024-02-10 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0033_autofilldispmodel_cus_dispatcher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autofilldispmodel',
            name='cus_dispatcher',
            field=models.CharField(default=None, max_length=100, verbose_name='Экспл.ведение'),
            preserve_default=False,
        ),
    ]