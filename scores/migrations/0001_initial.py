# Generated by Django 3.0.7 on 2020-06-06 19:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('athletes', '0001_initial'),
        ('wods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=50)),
                ('execution_date', models.DateField()),
                ('logging_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='athletes.Athlete')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wods.Workout')),
            ],
        ),
    ]
