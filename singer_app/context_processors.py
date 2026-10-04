from .models import SingerProfile, PerformanceCategory

def profile_context(request):
    """
    Global context processor supplying singer profile and navigation categories
    efficiently across all templates.
    """
    try:
        profile = SingerProfile.objects.first()
        if not profile:
            profile, _ = SingerProfile.objects.get_or_create(id=1)
            
        categories = PerformanceCategory.objects.only(
            'id', 'name', 'slug', 'icon', 'display_order'
        ).order_by('display_order', 'id')
    except Exception:
        profile = None
        categories = []

    return {
        'singer_profile': profile,
        'nav_categories': categories,
    }
