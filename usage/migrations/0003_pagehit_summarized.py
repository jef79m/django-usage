# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0002_auto_20151026_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagehit',
            name='summarized',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
