from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountyViewSet, MinistryViewSet, ProjectCategoryViewSet,
    ProjectViewSet, ProjectReportViewSet
)

router = DefaultRouter()
router.register(r'counties', CountyViewSet, basename='county')
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'categories', ProjectCategoryViewSet, basename='projectcategory')
router.register(r'', ProjectViewSet, basename='project')
router.register(r'reports', ProjectReportViewSet, basename='projectreport')

urlpatterns = [
    path('', include(router.urls)),
]
