# Generated by Django 4.0.6 on 2022-08-09 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='list_id',
            new_name='list',
        ),
    ]