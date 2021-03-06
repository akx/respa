# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-20 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0039_add_terms_of_use'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='reservation_confirmed_notification_extra',
            field=models.TextField(blank=True, verbose_name='Extra content to reservation confirmed notification'),
        ),
        migrations.AddField(
            model_name='resource',
            name='reservation_confirmed_notification_extra_en',
            field=models.TextField(blank=True, null=True, verbose_name='Extra content to reservation confirmed notification'),
        ),
        migrations.AddField(
            model_name='resource',
            name='reservation_confirmed_notification_extra_fi',
            field=models.TextField(blank=True, null=True, verbose_name='Extra content to reservation confirmed notification'),
        ),
        migrations.AddField(
            model_name='resource',
            name='reservation_confirmed_notification_extra_sv',
            field=models.TextField(blank=True, null=True, verbose_name='Extra content to reservation confirmed notification'),
        ),
    ]
