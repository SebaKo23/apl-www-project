from django import forms
from django.contrib import admin
from .models import User, Game, Rental, Review, Payment

class RentalAdminForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        return_date = cleaned_data.get("return_date")
        rent_date = cleaned_data.get("rent_date")
        if return_date and return_date < rent_date:
            raise forms.ValidationError("Data zwrotu nie może być wcześniejsza niż data wypożyczenia.")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'date_joined')
    ordering = ('-date_joined',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'platform', 'release_date', 'is_available')
    search_fields = ('title', 'genre', 'platform')
    list_filter = ('genre', 'platform', 'is_available')
    ordering = ('-release_date',)

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    form = RentalAdminForm
    list_display = ('id', 'user', 'game', 'rent_date', 'return_date', 'status')
    list_filter = ('status', 'rent_date', 'return_date')
    search_fields = ('user__username', 'game__title')
    ordering = ('-rent_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'rating', 'created_at')
    search_fields = ('user__username', 'game__title')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rental', 'amount', 'payment_date', 'payment_method')
    search_fields = ('user__username', 'rental__game__title')
    list_filter = ('payment_method', 'payment_date')
    ordering = ('-payment_date',)
