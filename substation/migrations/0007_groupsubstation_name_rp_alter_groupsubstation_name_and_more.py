# Generated by Django 4.2.7 on 2023-12-15 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('substation', '0006_remove_groupsubstation_group_engineer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsubstation',
            name='name_rp',
            field=models.CharField(blank=True, help_text='Нет кого? Чего?', max_length=64, null=True, verbose_name='Название группы ПС в родительском падеже'),
        ),
        migrations.AlterField(
            model_name='groupsubstation',
            name='name',
            field=models.CharField(help_text='Указываются группы ПС, ЦУС, предприятия, а также МЭС', max_length=64, unique=True, verbose_name='Название группы ПС'),
        ),
        migrations.AlterField(
            model_name='substation',
            name='group_substation',
            field=models.ForeignKey(blank=True, help_text='Прописываются только существующие группы ПС', null=True, on_delete=django.db.models.deletion.PROTECT, to='substation.groupsubstation', verbose_name='Группа подстанций'),
        ),
        migrations.AlterField(
            model_name='substation',
            name='name',
            field=models.CharField(help_text='Указываются только подстанции предприятия', max_length=64, unique=True, verbose_name='Название ПС'),
        ),
    ]
