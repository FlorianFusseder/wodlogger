# Generated by Django 3.0.7 on 2020-06-21 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_name', models.CharField(max_length=50)),
                ('movement_unit', models.CharField(choices=[('METERS', 'Meters'), ('REPS', 'Reps'), ('WEIGHT', 'kg'), ('REPS_AND_WEIGHT', 'Reps @ kg'), ('CALORIES', 'Calories')], default='REPS', max_length=20)),
                ('modality', models.CharField(choices=[('G', 'Gymnastics'), ('W', 'Wightlifiting'), ('M', 'Monostructural')], default='G', max_length=1)),
            ],
        ),
    ]
