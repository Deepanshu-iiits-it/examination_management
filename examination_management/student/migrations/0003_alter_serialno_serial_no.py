# Generated by Django 4.0.5 on 2022-11-23 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_serialno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serialno',
            name='serial_no',
            field=models.IntegerField(default=2022, verbose_name='Serial No'),
        ),
    ]
