# Generated by Django 4.1.2 on 2022-12-19 12:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_passwordresettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rank',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator, django.core.validators.MaxValueValidator]),
        ),
    ]
