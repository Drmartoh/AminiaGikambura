from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import GalleryItem
from .serializers import GalleryItemSerializer


class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.select_related('project', 'event').all()
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['media_type', 'project', 'event', 'year', 'is_featured', 'is_public']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated or not self.request.user.is_admin_user:
            queryset = queryset.filter(is_public=True)
        return queryset
