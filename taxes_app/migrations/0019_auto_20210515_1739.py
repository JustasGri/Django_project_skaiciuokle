# Generated by Django 3.2 on 2021-05-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes_app', '0018_alter_veikla_status2'),
    ]

    operations = [
        migrations.AddField(
            model_name='veikla',
            name='status3',
            field=models.CharField(choices=[('y', 'Taip'), ('n', 'NE')], default='n', help_text='Ar norite pasinaudoti sodros mokesčių lengvata?', max_length=1),
        ),
        migrations.AlterField(
            model_name='veikla',
            name='status2',
            field=models.CharField(choices=[('i30', 'Išlaidos 30%'), ('isf', 'Faktinės išlaidos')], default='isf', help_text='Pasirinkite išlaidas', max_length=3),
        ),
    ]
