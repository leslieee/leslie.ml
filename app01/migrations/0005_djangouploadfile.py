# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoUploadFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('headimg', models.FileField(upload_to=b'./upload/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
