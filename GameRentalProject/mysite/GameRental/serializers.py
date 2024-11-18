from rest_framework import serializers
from .models import User, Game, Rental, Review, Payment
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class GameSerializer(serializers.ModelSerializer):
    availability_status = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = '__all__'

    def get_availability_status(self, obj):
        return "Dostępna" if obj.is_available else "Niedostępna"

class RentalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    class Meta:
        model = Rental
        fields = '__all__'

    # Game availablility validation
    def validate(self, data):
        if not data['game'].is_available:
            raise serializers.ValidationError("Gra jest aktualnie niedostępna.")

        if data.get('return_date') and data['return_date'] < data['rent_date']:
            raise serializers.ValidationError("Data zwrotu nie może być wcześniejsza niż data wypożyczenia.")

        return data

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if not(1 <= value <= 5):
            raise serializers.ValidationError("Ocena musi być wartością od 1 do 5.")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    rental = serializers.PrimaryKeyRelatedField(queryset=Rental.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'