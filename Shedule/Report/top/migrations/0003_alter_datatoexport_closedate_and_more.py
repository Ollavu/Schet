# Generated by Django 4.0.6 on 2022-08-09 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('top', '0002_alter_closing_openid_alter_closing_statusid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatoexport',
            name='closedate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='top.closing', verbose_name='Закрыто'),
        ),
        migrations.AlterField(
            model_name='datatoexport',
            name='object_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='top.object', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='datatoexport',
            name='opendate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='top.opening', verbose_name='Окрыто'),
        ),
        migrations.AlterField(
            model_name='datatoexport',
            name='worker_fullname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='top.worker', verbose_name='ФИО'),
        ),
    ]