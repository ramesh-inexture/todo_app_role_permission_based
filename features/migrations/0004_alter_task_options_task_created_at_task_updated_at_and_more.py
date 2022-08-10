# Generated by Django 4.0.6 on 2022-08-10 06:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0003_alter_task_options_task_completed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={},
        ),
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 8, 10, 6, 27, 5, 128168, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tasklist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 8, 10, 6, 27, 5, 128168, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasklist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]