from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def absolute_media(url, request):
    """Return absolute URL for a media path (e.g. /media/site/logo.jpg) so images load reliably in production."""
    if not url:
        return url
    if request and getattr(request, 'build_absolute_uri', None):
        return request.build_absolute_uri(url)
    return url


@register.filter
def bold_youth_labour_office(value):
    """Wrap 'Youth Labour Office' in <strong> when present in address text."""
    if not value:
        return value
    return mark_safe(str(value).replace(
        'Youth Labour Office',
        '<strong>Youth Labour Office</strong>'
    ))
