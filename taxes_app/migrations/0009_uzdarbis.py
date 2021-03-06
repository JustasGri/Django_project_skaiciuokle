# Generated by Django 3.2 on 2021-05-09 11:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taxes_app', '0008_auto_20210509_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uzdarbis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pajamos', models.FloatField(max_length=100)),
                ('islaidos', models.FloatField(default=0, max_length=100)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('darbas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxes_app.veikla')),
            ],
        ),
    ]
