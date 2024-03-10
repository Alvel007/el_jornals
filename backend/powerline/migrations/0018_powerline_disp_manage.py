# Generated by Django 5.0.1 on 2024-02-01 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0017_remove_thirdpartydispatchers_dispatch_сenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='powerline',
            name='disp_manage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='disp_manage', to='powerline.dispatchcompanies', verbose_name='В управлении ДЦ'),
        ),
    ]
