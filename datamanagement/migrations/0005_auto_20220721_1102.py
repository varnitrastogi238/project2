# Generated by Django 2.2.14 on 2022-07-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagement', '0004_auto_20220721_0824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='strategy',
            old_name='working_days',
            new_name='working_days_1',
        ),
        migrations.RenameField(
            model_name='user1',
            old_name='working_days',
            new_name='working_days_1',
        ),
        migrations.AddField(
            model_name='strategy',
            name='working_days_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user1',
            name='working_days_2',
            field=models.IntegerField(default=0),
        ),
    ]
