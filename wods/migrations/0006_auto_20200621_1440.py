# Generated by Django 3.0.7 on 2020-06-21 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wods', '0005_auto_20200621_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workout',
            old_name='movement',
            new_name='components',
        ),
    ]
