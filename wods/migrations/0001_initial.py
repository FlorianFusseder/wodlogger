# Generated by Django 3.0.7 on 2020-06-20 13:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('athletes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(default='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('workout_type', models.CharField(choices=[('FOR_TIME', 'For Time'), ('AMRAP', 'AMRAP'), ('EMOM', 'EMOM'), ('LIFTING', 'Weightlifting'), ('REPS_SETS', 'Reps and Sets')], default='FOR_TIME', max_length=9)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='athletes.Athlete')),
            ],
        ),
    ]
