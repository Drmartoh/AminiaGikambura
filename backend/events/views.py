from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Event, EventRegistration, Announcement
from .serializers import (
    EventSerializer, EventRegistrationSerializer, EventRegistrationCreateSerializer,
    AnnouncementSerializer
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('county', 'project').all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event_type', 'county', 'project', 'is_published', 'is_featured', 'slug']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated or not self.request.user.is_admin_user:
            queryset = queryset.filter(is_published=True)
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        """Register for an event"""
        event = self.get_object()
        
        if event.is_full:
            return Response(
                {'error': 'Event is full'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if event.registration_deadline and timezone.now() > event.registration_deadline:
            return Response(
                {'error': 'Registration deadline has passed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already registered
        member = None
        if request.user.is_authenticated and hasattr(request.user, 'member_profile'):
            member = request.user.member_profile
            if EventRegistration.objects.filter(event=event, member=member).exists():
                return Response(
                    {'error': 'Already registered'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = EventRegistrationCreateSerializer(data={
            **request.data,
            'event': event.id,
        })
        serializer.is_valid(raise_exception=True)
        registration = serializer.save(member=member)
        
        return Response(
            EventRegistrationSerializer(registration).data,
            status=status.HTTP_201_CREATED
        )


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.select_related('event', 'member__user').all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'is_confirmed', 'payment_status']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return self.queryset
        if hasattr(user, 'member_profile'):
            return self.queryset.filter(member=user.member_profile)
        return self.queryset.none()


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_featured']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated or not self.request.user.is_admin_user:
            queryset = queryset.filter(is_published=True)
        return queryset
