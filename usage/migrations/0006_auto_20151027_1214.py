# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0005_auto_20151026_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usagesummary',
            old_name='time',
            new_name='hits',
        ),
    ]
