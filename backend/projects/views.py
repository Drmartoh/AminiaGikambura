from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import County, Ministry, ProjectCategory, Project, ProjectMember, ProjectReport
from .serializers import (
    CountySerializer, MinistrySerializer, ProjectCategorySerializer,
    ProjectSerializer, ProjectListSerializer, ProjectMemberSerializer,
    ProjectReportSerializer
)


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MinistryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'abbreviation']


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('category', 'county', 'ministry').prefetch_related('project_members', 'reports')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'county', 'ministry', 'is_featured', 'is_public', 'slug']
    search_fields = ['title', 'description', 'objectives']
    ordering_fields = ['created_at', 'start_date', 'budget_amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated or not self.request.user.is_admin_user:
            queryset = queryset.filter(is_public=True)
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def add_member(self, request, pk=None):
        """Add a member to a project"""
        project = self.get_object()
        member_id = request.data.get('member_id')
        role = request.data.get('role', 'member')
        
        from members.models import MemberProfile
        member = MemberProfile.objects.get(id=member_id)
        
        project_member, created = ProjectMember.objects.get_or_create(
            project=project,
            member=member,
            defaults={'role': role}
        )
        
        if not created:
            project_member.role = role
            project_member.is_active = True
            project_member.save()
        
        serializer = ProjectMemberSerializer(project_member)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a project"""
        project = self.get_object()
        members = project.project_members.filter(is_active=True)
        serializer = ProjectMemberSerializer(members, many=True)
        return Response(serializer.data)


class ProjectReportViewSet(viewsets.ModelViewSet):
    queryset = ProjectReport.objects.select_related('project')
    serializer_class = ProjectReportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'is_public']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated or not self.request.user.is_admin_user:
            queryset = queryset.filter(is_public=True)
        return queryset
