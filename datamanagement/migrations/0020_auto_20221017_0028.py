# Generated by Django 3.1.7 on 2022-10-16 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagement', '0019_auto_20221009_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='stop_symboll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.DateTimeField(default='_')),
            ],
        ),
        migrations.AddField(
            model_name='strategy',
            name='bb',
            field=models.IntegerField(default=20),
        ),
    ]
