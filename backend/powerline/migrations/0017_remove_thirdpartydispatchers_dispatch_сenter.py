# Generated by Django 5.0.1 on 2024-02-01 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0016_thirdpartydispatchers_disp_post_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thirdpartydispatchers',
            name='dispatch_сenter',
        ),
    ]
