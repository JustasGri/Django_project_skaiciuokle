# Generated by Django 3.2 on 2021-05-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes_app', '0020_auto_20210520_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='veikla',
            name='islaidos',
            field=models.FloatField(default=0, max_length=100, null=True),
        ),
    ]
