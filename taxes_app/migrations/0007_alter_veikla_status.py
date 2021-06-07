# Generated by Django 3.2 on 2021-05-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes_app', '0006_auto_20210506_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veikla',
            name='status',
            field=models.CharField(choices=[('p24', 'Pensija 2.4%'), ('p3', 'Pensija 3%'), ('pn', 'Nekaupiama')], default='pn', help_text='Ar kaupiate pensija?', max_length=3),
        ),
    ]