from django.urls import path
from .views import UserRegistrationView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
   
]