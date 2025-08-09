from django.urls import path
from .views import UserRegistrationView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
   
]