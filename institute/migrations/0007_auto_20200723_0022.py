# Generated by Django 3.0.6 on 2020-07-22 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0006_auto_20200723_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutestd',
            name='regd_no',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]