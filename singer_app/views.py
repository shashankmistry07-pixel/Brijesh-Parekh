from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from datetime import date
from .models import (
    SingerProfile, PerformanceCategory, GalleryItem, 
    ShowEvent, Testimonial, BookingInquiry
)
from .emails import send_inquiry_emails

UNAVAILABLE_GALLERY_MEDIA_PATHS = (
    "Vaidik Lagangeet/main.jpg",
    "Vaidik Lagangeet/video/w-4.MP4",
)

def home_view(request):
    """
    Optimized homepage view fetching featured media, performance categories,
    upcoming shows, and testimonials with zero N+1 queries.
    """
    profile = SingerProfile.objects.first()
    categories = PerformanceCategory.objects.all().order_by('display_order', 'id')
    
    # Query photos with category pre-joined
    all_photos = GalleryItem.objects.select_related('category').exclude(
        Q(image_path__iendswith='.mp4') | Q(image_path__iendswith='.mov')
    ).exclude(image_path__in=UNAVAILABLE_GALLERY_MEDIA_PATHS)
    featured_gallery = list(all_photos.filter(is_featured=True)[:8])
    if not featured_gallery:
        featured_gallery = list(all_photos[:8])
    
    # Query videos
    popular_videos = list(
        GalleryItem.objects.select_related('category').filter(
            Q(image_path__iendswith='.mp4') | Q(image_path__iendswith='.mov')
        ).exclude(image_path__in=UNAVAILABLE_GALLERY_MEDIA_PATHS).order_by('category__display_order', 'id')[:8]
    )
    
    # Upcoming live shows
    upcoming_events = list(
        ShowEvent.objects.select_related('category').filter(
            status='Upcoming', 
            event_date__gte=date.today()
        ).order_by('event_date')[:6]
    )
    if not upcoming_events:
        upcoming_events = list(
            ShowEvent.objects.select_related('category').all().order_by('-event_date')[:6]
        )
        
    testimonials = Testimonial.objects.all()[:6]

    context = {
        'profile': profile,
        'categories': categories,
        'featured_gallery': featured_gallery,
        'popular_videos': popular_videos,
        'upcoming_events': upcoming_events,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)


def about_view(request):
    """
    Profile and detailed biography view.
    """
    profile = SingerProfile.objects.first()
    categories = PerformanceCategory.objects.all().order_by('display_order', 'id')
    context = {
        'profile': profile,
        'categories': categories,
    }
    return render(request, 'about.html', context)


def services_view(request):
    """
    Performance services showcase view.
    """
    categories = PerformanceCategory.objects.all().order_by('display_order', 'id')
    return render(request, 'services.html', {'categories': categories})


def category_detail_view(request, slug):
    """
    Detailed performance category page with filtered photos, videos, and events.
    """
    category = get_object_or_404(PerformanceCategory, slug=slug)
    
    # Strictly separate photos and videos for this category
    category_photos = category.gallery_items.exclude(
        Q(image_path__iendswith='.mp4') | Q(image_path__iendswith='.mov')
    ).exclude(image_path__in=UNAVAILABLE_GALLERY_MEDIA_PATHS)
    category_videos = category.gallery_items.filter(
        Q(image_path__iendswith='.mp4') | Q(image_path__iendswith='.mov')
    ).exclude(image_path__in=UNAVAILABLE_GALLERY_MEDIA_PATHS)
    events = category.events.filter(status='Upcoming', event_date__gte=date.today()).order_by('event_date')
    
    context = {
        'category': category,
        'gallery_items': category_photos,
        'videos': category_videos,
        'events': events,
    }
    return render(request, 'category_detail.html', context)


def gallery_view(request):
    """
    High-resolution photo gallery with dynamic category filtering.
    """
    categories = PerformanceCategory.objects.all().order_by('display_order', 'id')
    selected_slug = request.GET.get('category', 'all').strip()
    
    photos = GalleryItem.objects.select_related('category').exclude(
        Q(image_path__iendswith='.mp4') | Q(image_path__iendswith='.mov')
    ).exclude(image_path__in=UNAVAILABLE_GALLERY_MEDIA_PATHS)
    
    if selected_slug and selected_slug != 'all':
        items = photos.filter(category__slug=selected_slug)
    else:
        items = photos
        
    context = {
        'categories': categories,
        'selected_category': selected_slug,
        'gallery_items': items,
    }
    return render(request, 'gallery.html', context)


def music_view(request):
    """
    Video tracks and live performances sampler with category filtering.
    """
    categories = PerformanceCategory.objects.all().order_by('display_order', 'id')
    selected_slug = request.GET.get('category', 'all').strip()
    
    videos_qs = GalleryItem.objects.select_related('category').filter(
        Q(image_path__iendswith='.mp4') | Q(image_path__iendswith='.mov')
    ).exclude(image_path__in=UNAVAILABLE_GALLERY_MEDIA_PATHS)
    if selected_slug and selected_slug != 'all':
        videos_qs = videos_qs.filter(category__slug=selected_slug)
        
    return render(request, 'music.html', {
        'videos': videos_qs, 
        'categories': categories,
        'selected_category': selected_slug
    })


def events_view(request):
    """
    Tour and live events schedule view (upcoming and past events).
    """
    upcoming = ShowEvent.objects.select_related('category').filter(
        event_date__gte=date.today()
    ).order_by('event_date')
    
    past = ShowEvent.objects.select_related('category').filter(
        event_date__lt=date.today()
    ).order_by('-event_date')
    
    return render(request, 'events.html', {'upcoming_events': upcoming, 'past_events': past})


def contact_view(request):
    """
    Contact and booking inquiry page with POST handler.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        event_type = request.POST.get('event_type', 'Garba & Navratri').strip()
        event_date_str = request.POST.get('event_date', '').strip()
        location = request.POST.get('location', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        event_date_val = None
        if event_date_str:
            try:
                event_date_val = date.fromisoformat(event_date_str)
            except ValueError:
                pass

        if name and email and phone and message:
            inquiry = BookingInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                event_type=event_type,
                event_date=event_date_val,
                location=location,
                subject=subject or f"Booking Inquiry from {name}",
                message=message
            )
            # Send notification to Admin and Confirmation to Client via Gmail SMTP
            send_inquiry_emails(inquiry, async_send=True)

            messages.success(
                request, 
                f"Thank you {name}! Your booking inquiry has been received. A confirmation email has been sent to {email}, and Brijesh Parekh's management team will contact you shortly."
            )
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields (Name, Email, Phone, Message).")

    profile = SingerProfile.objects.first()
    return render(request, 'contact.html', {'profile': profile})


@require_POST
def submit_inquiry_ajax(request):
    """
    Asynchronous AJAX booking inquiry handler with input validation.
    """
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    event_type = request.POST.get('event_type', 'Garba').strip()
    event_date_str = request.POST.get('event_date', '').strip()
    location = request.POST.get('location', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    if not name or not email or not phone or not message:
        return JsonResponse({
            'success': False, 
            'message': 'Please fill in all required fields (Name, Email, Phone, Message).'
        }, status=400)

    event_date_val = None
    if event_date_str:
        try:
            event_date_val = date.fromisoformat(event_date_str)
        except ValueError:
            pass

    try:
        inquiry = BookingInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            event_type=event_type,
            event_date=event_date_val,
            location=location,
            subject=subject or f"Booking Inquiry from {name}",
            message=message
        )
        # Send notification to Admin and Confirmation to Client via Gmail SMTP
        send_inquiry_emails(inquiry, async_send=True)

        return JsonResponse({
            'success': True, 
            'message': f'Thank you {name}! Your inquiry for {event_type} has been sent successfully. A confirmation email has been sent to {email}, and our team will get back to you soon!',
            'inquiry_id': inquiry.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'An unexpected error occurred while saving your inquiry. Please try calling directly.'
        }, status=500)


# ==========================================
# SEO & AI Web Crawlers (Robots & Sitemap)
# ==========================================
def robots_txt_view(request):
    """
    Dynamic robots.txt instructing Googlebot, Bingbot, and AI search engines.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /api/",
        "",
        "User-agent: Googlebot",
        "Allow: /",
        "",
        "User-agent: Bingbot",
        "Allow: /",
        "",
        "User-agent: Applebot",
        "Allow: /",
        "",
        "User-agent: GPTBot",
        "Allow: /",
        "",
        "User-agent: PerplexityBot",
        "Allow: /",
        "",
        "Sitemap: https://brijesh-parekh.vercel.app/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml_view(request):
    """
    Dynamic XML Sitemap for search engines with all active routes.
    """
    categories = PerformanceCategory.objects.all()
    today_str = date.today().isoformat()
    
    urls = [
        {'loc': 'https://brijesh-parekh.vercel.app/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': 'https://brijesh-parekh.vercel.app/about/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://brijesh-parekh.vercel.app/services/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://brijesh-parekh.vercel.app/events/', 'priority': '0.95', 'changefreq': 'daily'},
        {'loc': 'https://brijesh-parekh.vercel.app/gallery/', 'priority': '0.85', 'changefreq': 'weekly'},
        {'loc': 'https://brijesh-parekh.vercel.app/music/', 'priority': '0.85', 'changefreq': 'weekly'},
        {'loc': 'https://brijesh-parekh.vercel.app/contact/', 'priority': '0.9', 'changefreq': 'monthly'},
    ]
    
    for cat in categories:
        urls.append({
            'loc': f'https://brijesh-parekh.vercel.app/category/{cat.slug}/',
            'priority': '0.9',
            'changefreq': 'weekly'
        })
        
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for u in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{u["loc"]}</loc>')
        xml_parts.append(f'    <lastmod>{today_str}</lastmod>')
        xml_parts.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{u["priority"]}</priority>')
        xml_parts.append('  </url>')
    xml_parts.append('</urlset>')
    
    return HttpResponse("\n".join(xml_parts), content_type="application/xml")


# ==========================================
# Custom Error Views for Live Production
# ==========================================
def custom_404_view(request, exception=None):
    """
    Branded 404 Not Found error page.
    """
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """
    Branded 500 Server Error page.
    """
    return render(request, '500.html', status=500)
