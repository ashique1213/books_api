from django.urls import path
from .views import UserRegistrationView, UserProfileView,UserLogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/logout/', UserLogoutView.as_view(), name='user-logout'),
   
]