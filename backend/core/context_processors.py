def site_settings(request):
    try:
        from .models import SiteSettings
        settings = SiteSettings.load()
    except Exception:
        settings = None
    return {'site_settings': settings}


def section_styles(request):
    """Load all active section styles keyed by section_key for template use."""
    try:
        from .models import SectionStyle
        styles = SectionStyle.objects.filter(is_active=True).prefetch_related('slides').order_by('section_key')
        by_key = {s.section_key: s for s in styles}
    except Exception:
        by_key = {}
    return {'section_styles': by_key}
