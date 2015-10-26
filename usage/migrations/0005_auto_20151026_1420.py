# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0004_period_usagesummary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usagesummary',
            old_name='page',
            new_name='namespace',
        ),
        migrations.AddField(
            model_name='usagesummary',
            name='url_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
