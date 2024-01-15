# Generated by Django 5.0.1 on 2024-01-09 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_journal', '0034_alter_deviationscheme_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='deviationscheme',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_deviation', to=settings.AUTH_USER_MODEL, verbose_name='Запись сделал'),
        ),
    ]
