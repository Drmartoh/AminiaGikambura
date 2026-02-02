from rest_framework import serializers
from django.contrib.auth import get_user_model

# JWT serializers (optional)
try:
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    TokenObtainPairSerializer = None

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                  'phone_number', 'is_verified', 'is_approved', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'first_name', 'last_name', 'phone_number']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.role = 'member'  # Default role for registration
        user.save()
        return user


if JWT_AVAILABLE and TokenObtainPairSerializer:
    class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token['role'] = user.role
            token['is_approved'] = user.is_approved
            return token
else:
    class CustomTokenObtainPairSerializer(serializers.Serializer):
        pass  # Placeholder
