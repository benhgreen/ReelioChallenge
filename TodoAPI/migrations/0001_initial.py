# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=128)),
                ('hidden', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='lists',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='todoitem',
            name='list',
            field=models.ForeignKey(related_name='items',
                                    to='TodoAPI.TodoList'),
        ),
        migrations.AlterUniqueTogether(
            name='todolist',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='todoitem',
            unique_together=set([('list', 'text')]),
        ),
    ]
