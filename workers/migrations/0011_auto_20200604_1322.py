# Generated by Django 3.0.5 on 2020-06-04 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0010_auto_20200604_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workers',
            name='phone',
            field=models.CharField(max_length=12),
        ),
    ]
