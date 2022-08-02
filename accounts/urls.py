from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import AuthUserRegistrationView

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AuthUserRegistrationView.as_view(), name='user_registration'),
]