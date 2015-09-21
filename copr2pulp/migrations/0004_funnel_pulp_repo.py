# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copr2pulp', '0003_feed_pulp_repo'),
    ]

    operations = [
        migrations.AddField(
            model_name='funnel',
            name='pulp_repo',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
