# Generated by Django 3.0.5 on 2020-05-31 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officials', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watercan',
            old_name='count',
            new_name='receieved',
        ),
        migrations.AddField(
            model_name='watercan',
            name='given',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
