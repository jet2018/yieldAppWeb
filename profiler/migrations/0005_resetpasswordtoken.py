# Generated by Django 3.1.7 on 2021-08-17 07:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiler', '0004_remove_profile_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPasswordToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('generated_on', models.DateTimeField(auto_now=True)),
                ('expires_on', models.DateTimeField(default=datetime.datetime(2021, 8, 17, 7, 33, 19, 754750))),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
