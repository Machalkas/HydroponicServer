# Generated by Django 3.2 on 2022-02-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farms', '0008_auto_20211201_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='record_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата записи'),
        ),
    ]
