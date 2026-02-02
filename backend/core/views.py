from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# JWT imports (optional)
try:
    from rest_framework_simplejwt.views import TokenObtainPairView
    from .serializers import CustomTokenObtainPairSerializer
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Register a new user (member)
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification email (via Celery task)
        # send_verification_email.delay(user.id)
        
        return Response({
            'message': 'Registration successful. Please wait for admin approval.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


if JWT_AVAILABLE:
    class CustomTokenObtainPairView(TokenObtainPairView):
        serializer_class = CustomTokenObtainPairSerializer
else:
    # Fallback view if JWT is not available
    class CustomTokenObtainPairView(generics.GenericAPIView):
        def post(self, request):
            return Response({'error': 'JWT authentication not configured'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user details
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
