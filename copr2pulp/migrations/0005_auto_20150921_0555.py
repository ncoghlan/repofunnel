# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copr2pulp', '0004_funnel_pulp_repo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='feed_url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='funnel',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
