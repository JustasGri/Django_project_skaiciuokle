# Generated by Django 3.2 on 2021-05-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes_app', '0012_auto_20210511_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uzdarbis',
            name='islaidos',
            field=models.FloatField(default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='uzdarbis',
            name='pajamos',
            field=models.FloatField(default=0, max_length=100, null=True),
        ),
    ]
