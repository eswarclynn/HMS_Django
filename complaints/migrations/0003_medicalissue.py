# Generated by Django 3.0.6 on 2020-09-21 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0002_complaint_complainee'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(choices=[('Student', 'Student'), ('Official', 'Official'), ('Worker', 'Worker')], max_length=40)),
                ('entity_id', models.IntegerField()),
                ('status', models.CharField(choices=[('Registered', 'Registered'), ('Resolved', 'Resolved')], default='Registered', max_length=20)),
                ('summary', models.CharField(max_length=200)),
                ('detailed', models.TextField()),
                ('remark', models.TextField(blank=True, null=True)),
            ],
        ),
    ]