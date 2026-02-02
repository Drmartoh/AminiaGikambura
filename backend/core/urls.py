from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, current_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('me/', current_user, name='current_user'),
]
