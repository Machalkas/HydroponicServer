# Generated by Django 3.2 on 2021-05-16 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Farms', '0004_alter_timetable_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='farm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Farms.farm', verbose_name='Ферма'),
        ),
    ]
