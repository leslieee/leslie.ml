# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_djangouploadfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='djangouploadfile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
