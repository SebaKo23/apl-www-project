from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..models import User as CustomUser, Game, Rental, Review, Payment
from django.utils import timezone

class GameRentalAPITests(APITestCase):

    def setUp(self):
        self.custom_user = CustomUser.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            is_staff=False,
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        token = Token.objects.create(user=self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.game = Game.objects.create(
            title="Test Game",
            genre="Action",
            platform="PC",
            release_date="2020-01-01",
            is_available=True,
        )

        self.rental = Rental.objects.create(user=self.custom_user, game=self.game, rent_date=timezone.now())

        self.review = Review.objects.create(user=self.custom_user, game=self.game, rating=4, comment="Great game!")

        self.payment = Payment.objects.create(
            user=self.custom_user, rental=self.rental, amount=50.00, payment_method="Credit Card"
        )

    # Testy rejestracji
    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    # Testy rejestracji użytkownika bez hasła
    def test_register_user_without_password(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    # Testy logowania
    def test_login_user(self):
        url = reverse('login')
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"], "testuser")

    # Test endpointu listującego gry zaczynające się na daną literę
    def test_games_by_title(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("games-by-title", args=["T"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test endpointu listującego wypożyczenia użytkownika
    def test_user_rentals(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("user-rentals", args=[self.custom_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test CRUD endpointu dla modelu Review (Create)
    def test_create_review(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("review-list")
        data = {
            "user": self.custom_user.id,
            "game": self.game.id,
            "rating": 5,
            "comment": "Amazing game!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test CRUD endpointu dla modelu Rental (Create)
    def test_create_rental(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("rental-list")
        data = {
            "user": self.custom_user.id,
            "game": self.game.id,
            "rent_date": timezone.now()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test CRUD endpointu dla modelu Game (Delete)
    def test_delete_game(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("game-detail", args=[self.game.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test CRUD endpointu dla modelu Payment (Update)
    def test_update_payment(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("payment-detail", args=[self.payment.id])
        data = {
            "amount": 60.00,
            "payment_method": "Debit Card"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "60.00")

    # Test walidacyjne daty zwrotu
    def test_rental_return_date_validation(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse('rental-list')
        data = {
            "user": self.custom_user.id,
            "game": self.game.id,
            "rent_date": "2024-11-01T10:00:00Z",
            "return_date": "2024-10-31T10:00:00Z"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Data zwrotu nie może być wcześniejsza niż data wypożyczenia", str(response.data))

# Testy zestawienia zamówień
class MonthlyOrdersSummaryTests(APITestCase):

    def setUp(self):
        self.custom_user = CustomUser.objects.create(
            username="admin",
            email="admin@example.com",
            password="admin123",
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="admin123",
            is_staff = True
        )

        token = Token.objects.create(user=self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


        self.game1 = Game.objects.create(
            title="Game 1",
            genre="Action",
            platform="PC",
            release_date=timezone.datetime(2022, 1, 1, tzinfo=timezone.utc)
        )

        self.game2 = Game.objects.create(
            title="Game 2",
            genre="Action",
            platform="PC",
            release_date=timezone.datetime(2022, 1, 1, tzinfo=timezone.utc)
        )

        self.rental1 = Rental.objects.create(
            user=self.custom_user,
            game=self.game1,
            rent_date=timezone.datetime(2024, 11, 1, tzinfo=timezone.utc)
        )
        self.rental2 = Rental.objects.create(
            user=self.custom_user,
            game=self.game2,
            rent_date=timezone.datetime(2024, 11, 5, tzinfo=timezone.utc)
        )

    def test_monthly_orders_summary_with_no_data(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse('monthly-orders-summary')
        response = self.client.get(url, {"month": "12", "year": "2024"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_monthly_orders_summary_with_data(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse('monthly-orders-summary')
        response = self.client.get(url, {"month": "11", "year": "2024"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn("total_rentals", response.data[0])
