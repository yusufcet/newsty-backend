# Generated by Django 4.1.2 on 2022-12-09 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_hashtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]