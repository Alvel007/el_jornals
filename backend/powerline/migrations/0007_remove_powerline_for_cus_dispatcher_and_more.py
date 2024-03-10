# Generated by Django 5.0.1 on 2024-01-31 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0006_powerline_for_cus_dispatcher'),
        ('substation', '0002_alter_substation_dispatcher_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='powerline',
            name='for_CUS_dispatcher',
        ),
        migrations.AddField(
            model_name='powerline',
            name='for_CUS_dispatcher',
            field=models.ManyToManyField(blank=True, help_text='Какому диспетчеру интересна эта ВЛ', limit_choices_to={'dispatch_point': True}, null=True, to='substation.substation', verbose_name='Интересна диспетчеру'),
        ),
    ]