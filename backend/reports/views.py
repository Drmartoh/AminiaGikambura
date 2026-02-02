from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Report, ContactMessage
from .serializers import (
    ReportSerializer, ContactMessageSerializer, ContactMessageCreateSerializer
)


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Report.objects.select_related('project').all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report_type', 'project', 'is_public']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated or not self.request.user.is_admin_user:
            queryset = queryset.filter(is_public=True)
        return queryset


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_admin_user:
            return self.queryset
        # Public users can only create, not view
        return self.queryset.none()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Thank you for your message. We will get back to you soon.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
