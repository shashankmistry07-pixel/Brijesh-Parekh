from .models import SingerProfile, PerformanceCategory

def profile_context(request):
    profile, _ = SingerProfile.objects.get_or_create(id=1)
    categories = PerformanceCategory.objects.all()
    return {
        'singer_profile': profile,
        'nav_categories': categories,
    }
