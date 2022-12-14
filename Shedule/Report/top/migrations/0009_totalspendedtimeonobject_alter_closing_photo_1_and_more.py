# Generated by Django 4.0.6 on 2022-08-10 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('top', '0008_alter_datatoexport_spended_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalSpendedTimeOnObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_fullname', models.CharField(max_length=150, verbose_name='ФИО')),
                ('object_name', models.CharField(max_length=150, verbose_name='Объект')),
                ('opendate', models.DateField(verbose_name='Окрыто')),
                ('closedate', models.DateField(verbose_name='Закрыто')),
                ('spended_time', models.TimeField(max_length=25, verbose_name='Затраченное время')),
            ],
            options={
                'verbose_name': 'Суммарное время на объекте в Excel',
                'verbose_name_plural': 'Суммарное время на объекте в Excel',
            },
        ),
        migrations.AlterField(
            model_name='closing',
            name='photo_1',
            field=models.ImageField(blank=True, upload_to='photos/2022/08/10/', verbose_name='Фото 1'),
        ),
        migrations.AlterField(
            model_name='closing',
            name='photo_2',
            field=models.ImageField(blank=True, upload_to='photos/2022/08/10/', verbose_name='Фото 2'),
        ),
        migrations.AlterField(
            model_name='closing',
            name='photo_3',
            field=models.ImageField(blank=True, upload_to='photos/2022/08/10/', verbose_name='Фото 3'),
        ),
    ]
