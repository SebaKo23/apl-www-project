from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (MonthlyOrdersSummaryView, RegisterUser, UserRentals, GamesByTitle,
                    UserViewSet, GameViewSet, RentalViewSet, ReviewViewSet, PaymentViewSet, LoginUser)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'games', GameViewSet, basename='game')
router.register(r'rentals', RentalViewSet, basename='rental')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('monthly-orders-summary/', MonthlyOrdersSummaryView.as_view(), name='monthly-orders-summary'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('user-rentals/<int:user_id>/', UserRentals.as_view(), name='user-rentals'),
    path('games-by-title/<str:letter>/', GamesByTitle.as_view(), name='games-by-title'),
    path('', include(router.urls)),
]
