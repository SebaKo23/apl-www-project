# Generated by Django 4.2.16 on 2024-10-25 18:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='Title', max_length=255)),
                ('genre', models.CharField(db_column='Genre', max_length=100)),
                ('platform', models.CharField(db_column='Platform', max_length=50)),
                ('release_date', models.DateField(db_column='Release_date')),
                ('is_available', models.BooleanField(db_column='Is_available', default=True)),
            ],
            options={
                'db_table': 'Game',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='Username', max_length=150, unique=True)),
                ('email', models.CharField(db_column='Email', max_length=255, unique=True)),
                ('password', models.CharField(db_column='Password', max_length=128)),
                ('is_staff', models.BooleanField(db_column='Is_staff', default=False)),
                ('date_joined', models.DateTimeField(db_column='Date_joined', default=datetime.datetime.now)),
                ('last_login', models.DateTimeField(blank=True, db_column='Last_login', null=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('rating', models.IntegerField(db_column='Rating')),
                ('comment', models.TextField(blank=True, db_column='Comment', null=True)),
                ('created_at', models.DateTimeField(db_column='Created_at', default=datetime.datetime.now)),
                ('game', models.ForeignKey(db_column='Game_id', on_delete=django.db.models.deletion.DO_NOTHING, to='GameRental.game')),
                ('user', models.ForeignKey(db_column='User_id', on_delete=django.db.models.deletion.DO_NOTHING, to='GameRental.user')),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('rent_date', models.DateTimeField(db_column='Rent_date', default=datetime.datetime.now)),
                ('return_date', models.DateTimeField(blank=True, db_column='Return_date', null=True)),
                ('status', models.CharField(db_column='Status', default='wypożyczona', max_length=20)),
                ('game', models.ForeignKey(db_column='Game_id', on_delete=django.db.models.deletion.DO_NOTHING, to='GameRental.game')),
                ('user', models.ForeignKey(db_column='User_id', on_delete=django.db.models.deletion.DO_NOTHING, to='GameRental.user')),
            ],
            options={
                'db_table': 'Rental',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('amount', models.DecimalField(db_column='Amount', decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(db_column='Payment_date', default=datetime.datetime.now)),
                ('payment_method', models.CharField(db_column='Payment_method', max_length=50)),
                ('rental', models.ForeignKey(db_column='Rental_id', on_delete=django.db.models.deletion.DO_NOTHING, to='GameRental.rental')),
                ('user', models.ForeignKey(db_column='User_id', on_delete=django.db.models.deletion.DO_NOTHING, to='GameRental.user')),
            ],
            options={
                'db_table': 'Payment',
            },
        ),
    ]
