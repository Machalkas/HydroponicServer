# Generated by Django 3.2 on 2021-05-18 13:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Farms', '0005_alter_parameters_farm'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='farm',
            unique_together={('name', 'user')},
        ),
    ]