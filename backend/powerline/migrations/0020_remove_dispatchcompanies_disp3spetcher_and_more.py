# Generated by Django 5.0.1 on 2024-02-01 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0019_dispatchcompanies_disp3spetcher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispatchcompanies',
            name='disp3spetcher',
        ),
        migrations.AddField(
            model_name='dispatchcompanies',
            name='disp3spetcher',
            field=models.ManyToManyField(blank=True, to='powerline.thirdpartydispatchers', verbose_name='Диспетчер'),
        ),
    ]
