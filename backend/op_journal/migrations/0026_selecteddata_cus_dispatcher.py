# Generated by Django 5.0.1 on 2024-02-05 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0025_remove_selecteddata_cus_dispatcher'),
    ]

    operations = [
        migrations.AddField(
            model_name='selecteddata',
            name='cus_dispatcher',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Экспл.ведение'),
        ),
    ]