from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import FundingSource, Sponsor, Donation, DonationTier
from .serializers import (
    FundingSourceSerializer, SponsorSerializer, DonationSerializer,
    DonationCreateSerializer, DonationTierSerializer
)


class FundingSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FundingSource.objects.select_related('ministry', 'county').all()
    serializer_class = FundingSourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['source_type', 'ministry', 'county']


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.filter(is_active=True)
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.select_related('project', 'sponsor').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'payment_method', 'project', 'currency']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DonationCreateSerializer
        return DonationSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_admin_user:
            return self.queryset
        # Public users can only see completed donations (anonymous if requested)
        return self.queryset.filter(status='completed')
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_completed(self, request, pk=None):
        """Mark a donation as completed"""
        donation = self.get_object()
        donation.status = 'completed'
        donation.save()
        
        # Send receipt email (via Celery task)
        # send_donation_receipt.delay(donation.id)
        
        return Response({'message': 'Donation marked as completed'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get donation statistics"""
        total_donations = Donation.objects.filter(status='completed').count()
        total_amount = sum(
            d.amount for d in Donation.objects.filter(status='completed')
        )
        
        return Response({
            'total_donations': total_donations,
            'total_amount': total_amount,
        })


class DonationTierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DonationTier.objects.filter(is_active=True).select_related('project')
    serializer_class = DonationTierSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']
