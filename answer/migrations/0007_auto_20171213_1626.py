# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-13 07:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0006_auto_20171213_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statisticage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='statisticlist',
            options={},
        ),
        migrations.AddField(
            model_name='statisticage',
            name='id',
            field=models.AutoField(auto_created=True, default=django.utils.timezone.now, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statisticlist',
            name='id',
            field=models.AutoField(auto_created=True, default=type, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
