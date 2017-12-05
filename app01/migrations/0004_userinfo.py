# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20160526_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=20)),
                ('Phone', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
