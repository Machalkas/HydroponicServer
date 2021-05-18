# Generated by Django 3.2 on 2021-05-18 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Farms', '0006_alter_farm_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='statistic',
            unique_together={('record_date', 'farm')},
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together={('date', 'farm')},
        ),
    ]