# Generated by Django 3.0.6 on 2020-05-30 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('second_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_description', models.TextField(default='')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wods.Athlete')),
            ],
        ),
    ]