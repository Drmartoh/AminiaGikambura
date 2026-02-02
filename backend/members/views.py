from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MemberProfile, Certificate
from .serializers import MemberProfileSerializer, MemberProfileCreateSerializer, CertificateSerializer
from core.models import User


class MemberProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for member profiles
    """
    queryset = MemberProfile.objects.select_related('user', 'county').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MemberProfileCreateSerializer
        return MemberProfileSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return self.queryset
        return self.queryset.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile, created = MemberProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Approve a member registration"""
        profile = self.get_object()
        profile.user.is_approved = True
        profile.user.save()
        return Response({'message': 'Member approved successfully'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """Reject a member registration"""
        profile = self.get_object()
        profile.user.is_approved = False
        profile.user.save()
        return Response({'message': 'Member rejected'})


class CertificateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for certificates
    """
    queryset = Certificate.objects.select_related('member__user').all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return self.queryset
        profile = get_object_or_404(MemberProfile, user=user)
        return self.queryset.filter(member=profile)
