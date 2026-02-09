from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def bold_youth_labour_office(value):
    """Wrap 'Youth Labour Office' in <strong> when present in address text."""
    if not value:
        return value
    return mark_safe(str(value).replace(
        'Youth Labour Office',
        '<strong>Youth Labour Office</strong>'
    ))
