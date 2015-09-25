# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copr2pulp', '0005_auto_20150921_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='funnel',
            name='funnel_url',
            field=models.URLField(null=True, unique=True),
        ),
    ]
