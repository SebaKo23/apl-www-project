from django.db import models
from datetime import datetime

class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    username = models.CharField(db_column='Username', max_length=150, unique=True, null=False)
    email = models.CharField(db_column='Email', max_length=255, unique=True, null=False)
    password = models.CharField(db_column='Password', max_length=128, null=False)
    is_staff = models.BooleanField(db_column='Is_staff', default=False, null=False)
    date_joined = models.DateTimeField(db_column='Date_joined', default=datetime.now, null=False)
    last_login = models.DateTimeField(db_column='Last_login', blank=True, null=True)



class Game(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    title = models.CharField(db_column='Title', max_length=255, null=False)
    genre = models.CharField(db_column='Genre', max_length=100, null=False)
    platform = models.CharField(db_column='Platform', max_length=50, null=False)
    release_date = models.DateField(db_column='Release_date', null=False)
    is_available = models.BooleanField(db_column='Is_available', default=True, null=False)



class Rental(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_id', null=False)
    game = models.ForeignKey(Game, models.DO_NOTHING, db_column='Game_id', null=False)
    rent_date = models.DateTimeField(db_column='Rent_date', default=datetime.now, null=False)
    return_date = models.DateTimeField(db_column='Return_date', blank=True, null=True)
    status = models.CharField(db_column='Status', default='wypożyczona', max_length=20, null=False)



class Review(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_id', null=False)
    game = models.ForeignKey(Game, models.DO_NOTHING, db_column='Game_id', null=False)
    rating = models.IntegerField(db_column='Rating', null=False)
    comment = models.TextField(db_column='Comment', blank=True, null=True)
    created_at = models.DateTimeField(db_column='Created_at', default=datetime.now, null=False)



class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_id', null=False)
    rental = models.ForeignKey('Rental', models.DO_NOTHING, db_column='Rental_id', null=False)
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateTimeField(db_column='Payment_date', default=datetime.now, null=False)
    payment_method = models.CharField(db_column='Payment_method', max_length=50, null=False)
