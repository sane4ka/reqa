# Generated by Django 4.2.1 on 2023-05-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_jiraissue'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]