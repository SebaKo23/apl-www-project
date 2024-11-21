from django.contrib.auth import authenticate
from django.contrib.auth.models import User as AuthUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import User, Game, Rental, Review, Payment
from .serializers import UserSerializer, GameSerializer, RentalSerializer, ReviewSerializer, PaymentSerializer
from .permissions import IsAdminOrOwner, IsOwnerOrReadOnly
from datetime import datetime
from django.db.models import Count


# Rejestracja użytkownika
class RegisterUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            game_rental_user = serializer.save()

            auth_user = AuthUser.objects.create_user(
                username=game_rental_user.username,
                email=game_rental_user.email,
                password=request.data.get('password')
            )

            return Response({"message": "Użytkownik zarejestrowany pomyślnie!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logowanie użytkownika
class LoginUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Nieprawidłowe dane uwierzytelniania"}, status=status.HTTP_401_UNAUTHORIZED)


# Zestawienie miesięczne zamówień
class MonthlyOrdersSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        month = request.query_params.get('month', datetime.now().month)
        year = request.query_params.get('year', datetime.now().year)

        try:
            month = int(month)
            year = int(year)
            if not (1 <= month <= 12):
                raise ValueError("Miesiąc musi być liczbą od 1 do 12.")
        except ValueError:
            return Response({"error": "Nieprawidłowe parametry miesiąca lub roku."}, status=status.HTTP_400_BAD_REQUEST)

        rentals = Rental.objects.filter(
            rent_date__year=year, rent_date__month=month
        ).values('game__title').annotate(total=Count('id'))

        summary = [{"title": r['game__title'], "total_rentals": r['total']} for r in rentals]
        return Response(summary, status=status.HTTP_200_OK)


# User CRUD
class UserViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Lista gier zaczynająca się na określoną literę
class GamesByTitle(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, letter):
        games = Game.objects.filter(title__istartswith=letter)
        if not games.exists():
            return Response({"message": "Brak gier zaczynających się na podaną literę."}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

# Game CRUD
class GameViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Game.objects.all()
    serializer_class = GameSerializer

# Lista wypożyczeń użytkownika
class UserRentals(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request, user_id):
        rentals = Rental.objects.filter(user_id=user_id)
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)

# Rental CRUD
class RentalViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Rental.objects.all()
        return Rental.objects.filter(user=self.request.user)

# Review CRUD
class ReviewViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        custom_user = User.objects.get(username=self.request.user.username)
        serializer.save(user=custom_user)

# Payment CRUD
class PaymentViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        custom_user = User.objects.get(username=self.request.user.username)
        return Payment.objects.filter(user=custom_user)