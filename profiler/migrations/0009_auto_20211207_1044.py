# Generated by Django 3.2.4 on 2021-12-07 10:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profiler', '0008_auto_20211207_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatecodes',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 7, 11, 14, 55, 243507, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='generatecodes',
            name='token',
            field=models.CharField(default='873895', max_length=100, unique=True),
        ),
    ]
