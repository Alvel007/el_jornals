# Generated by Django 5.0.1 on 2024-02-03 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerline', '0032_remove_powerline_for_cus_dispatcher'),
        ('substation', '0002_alter_substation_dispatcher_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='powerline',
            name='for_CUS_dispatcher',
            field=models.ManyToManyField(blank=True, help_text='В эксплуатационной ответственности какого диспетчера находится указанная ВЛ?', limit_choices_to={'dispatch_point': True}, related_name='dispatcher_interests', to='substation.substation', verbose_name='Интересна диспетчеру'),
        ),
    ]