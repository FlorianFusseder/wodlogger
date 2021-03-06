# Generated by Django 3.0.7 on 2020-07-04 07:31

from django.db import migrations, models
import django.db.models.deletion


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
                ('has_weight', models.BooleanField()),
                ('has_distance', models.BooleanField()),
                ('has_height', models.BooleanField()),
                ('modality', models.CharField(choices=[('G', 'Gymnastics'), ('W', 'Wightlifiting'), ('M', 'Monostructural')], default='G', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.PositiveSmallIntegerField(default=1)),
                ('max_reps', models.BooleanField(default=False)),
                ('kg_m', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('kg_f', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('distance', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('timespan', models.DurationField(blank=True, null=True)),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wodmovements.Movement')),
            ],
        ),
    ]
