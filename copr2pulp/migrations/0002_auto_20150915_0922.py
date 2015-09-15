# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copr2pulp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('feed_url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='funnel',
            name='feeds',
            field=models.ManyToManyField(to='copr2pulp.Feed'),
        ),
    ]
