from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint - lists all available endpoints
    """
    return Response({
        'auth': {
            'register': reverse('register', request=request, format=format),
            'login': reverse('token_obtain_pair', request=request, format=format),
            'refresh': reverse('token_refresh', request=request, format=format),
            'current_user': reverse('current_user', request=request, format=format),
        },
        'members': reverse('memberprofile-list', request=request, format=format),
        'projects': reverse('project-list', request=request, format=format),
        'events': reverse('event-list', request=request, format=format),
        'funding': reverse('donation-list', request=request, format=format),
        'gallery': reverse('galleryitem-list', request=request, format=format),
        'sports': reverse('sportprogram-list', request=request, format=format),
        'gamification': reverse('badge-list', request=request, format=format),
        'reports': reverse('report-list', request=request, format=format),
        'message': 'AGCBO Digital Hub API - Welcome!',
    })
