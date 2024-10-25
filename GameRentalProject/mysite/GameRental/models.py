from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError

class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    username = models.CharField(db_column='Username', max_length=150, unique=True, null=False)
    email = models.CharField(db_column='Email', max_length=255, unique=True, null=False)
    password = models.CharField(db_column='Password', max_length=128, null=False)
    is_staff = models.BooleanField(db_column='Is_staff', default=False, null=False)
    date_joined = models.DateTimeField(db_column='Date_joined', default=datetime.now, null=False)
    last_login = models.DateTimeField(db_column='Last_login', blank=True, null=True)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return f"{self.username} ({self.email})"

class AvailableGamesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)

class Game(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    title = models.CharField(db_column='Title', max_length=255, null=False)
    genre = models.CharField(db_column='Genre', max_length=100, null=False)
    platform = models.CharField(db_column='Platform', max_length=50, null=False)
    release_date = models.DateField(db_column='Release_date', null=False)
    is_available = models.BooleanField(db_column='Is_available', default=True, null=False)
    objects = models.Manager()
    available = AvailableGamesManager()

    class Meta:
        db_table = 'Game'

    def __str__(self):
        return self.title

class Rental(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_id', null=False)
    game = models.ForeignKey(Game, models.DO_NOTHING, db_column='Game_id', null=False)
    rent_date = models.DateTimeField(db_column='Rent_date', default=datetime.now, null=False)
    return_date = models.DateTimeField(db_column='Return_date', blank=True, null=True)
    status = models.CharField(db_column='Status', default='wypożyczona', max_length=20, null=False)

    class Meta:
        db_table = 'Rental'

    @classmethod
    def active_rentals(cls):
        return cls.objects.filter(status='wypożyczona')

    def save(self, *args, **kwargs):
        if self.status == "zwrócona" and not self.return_date:
            self.return_date = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} wypożyczył {self.game}"

class Review(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_id', null=False)
    game = models.ForeignKey(Game, models.DO_NOTHING, db_column='Game_id', null=False)
    rating = models.IntegerField(db_column='Rating', null=False)
    comment = models.TextField(db_column='Comment', blank=True, null=True)
    created_at = models.DateTimeField(db_column='Created_at', default=datetime.now, null=False)

    class Meta:
        db_table = 'Review'

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating musi być w zakresie od 1 do 5.')

    def __str__(self):
        return f"Recenzja: {self.game} przez {self.user} ({self.rating}/5)"

class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_id', null=False)
    rental = models.ForeignKey('Rental', models.DO_NOTHING, db_column='Rental_id', null=False)
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateTimeField(db_column='Payment_date', default=datetime.now, null=False)
    payment_method = models.CharField(db_column='Payment_method', max_length=50, null=False)

    class Meta:
        db_table = 'Payment'

    def __str__(self):
        return f"Płatność {self.amount} PLN dla {self.user}"
