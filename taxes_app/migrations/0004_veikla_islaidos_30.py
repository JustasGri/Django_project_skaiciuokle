# Generated by Django 3.2 on 2021-05-04 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes_app', '0003_veikla_islaidos'),
    ]

    operations = [
        migrations.AddField(
            model_name='veikla',
            name='islaidos_30',
            field=models.BooleanField(default=True),
        ),
    ]
