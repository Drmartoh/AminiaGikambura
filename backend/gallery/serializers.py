from rest_framework import serializers
from .models import GalleryItem
from projects.serializers import ProjectListSerializer
from events.serializers import EventSerializer


class GalleryItemSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryItem
        fields = ['id', 'title', 'description', 'media_type', 'file', 'thumbnail',
                  'url', 'project', 'event', 'year', 'tags', 'tags_list',
                  'is_featured', 'is_public', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_tags_list(self, obj):
        return [t.strip() for t in obj.tags.split(',')] if obj.tags else []
