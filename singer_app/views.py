from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import date
from .models import (
    SingerProfile, PerformanceCategory, GalleryItem, 
    AudioTrack, ShowEvent, Testimonial, BookingInquiry
)

def home_view(request):
    profile = SingerProfile.objects.first()
    categories = PerformanceCategory.objects.all()
    featured_gallery = GalleryItem.objects.filter(is_featured=True)[:8]
    if not featured_gallery:
        featured_gallery = GalleryItem.objects.all()[:8]
    
    popular_tracks = AudioTrack.objects.all()[:6]
    upcoming_events = ShowEvent.objects.filter(status='Upcoming', event_date__gte=date.today())[:4]
    if not upcoming_events:
        upcoming_events = ShowEvent.objects.all()[:4]
        
    testimonials = Testimonial.objects.all()

    context = {
        'profile': profile,
        'categories': categories,
        'featured_gallery': featured_gallery,
        'popular_tracks': popular_tracks,
        'upcoming_events': upcoming_events,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about_view(request):
    profile = SingerProfile.objects.first()
    categories = PerformanceCategory.objects.all()
    context = {
        'profile': profile,
        'categories': categories,
    }
    return render(request, 'about.html', context)

def services_view(request):
    categories = PerformanceCategory.objects.all()
    return render(request, 'services.html', {'categories': categories})

def category_detail_view(request, slug):
    category = get_object_or_404(PerformanceCategory, slug=slug)
    gallery_items = category.gallery_items.all()
    tracks = category.tracks.all()
    events = category.events.filter(status='Upcoming')
    
    context = {
        'category': category,
        'gallery_items': gallery_items,
        'tracks': tracks,
        'events': events,
    }
    return render(request, 'category_detail.html', context)

def gallery_view(request):
    categories = PerformanceCategory.objects.all()
    selected_slug = request.GET.get('category', 'all')
    
    if selected_slug and selected_slug != 'all':
        items = GalleryItem.objects.filter(category__slug=selected_slug)
    else:
        items = GalleryItem.objects.all()
        
    context = {
        'categories': categories,
        'selected_category': selected_slug,
        'gallery_items': items,
    }
    return render(request, 'gallery.html', context)

def music_view(request):
    tracks = AudioTrack.objects.all()
    categories = PerformanceCategory.objects.all()
    return render(request, 'music.html', {'tracks': tracks, 'categories': categories})

def events_view(request):
    upcoming = ShowEvent.objects.filter(event_date__gte=date.today()).order_by('event_date')
    past = ShowEvent.objects.filter(event_date__lt=date.today()).order_by('-event_date')
    return render(request, 'events.html', {'upcoming_events': upcoming, 'past_events': past})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        event_type = request.POST.get('event_type', 'Garba & Navratri')
        event_date_str = request.POST.get('event_date', None)
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
            BookingInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                event_type=event_type,
                event_date=event_date_val,
                location=location,
                subject=subject or f"Booking Inquiry from {name}",
                message=message
            )
            messages.success(request, f"Thank you {name}! Your booking inquiry has been received. Brijesh Parekh's team will contact you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields (Name, Email, Phone, Message).")

    profile = SingerProfile.objects.first()
    return render(request, 'contact.html', {'profile': profile})

@require_POST
def submit_inquiry_ajax(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    event_type = request.POST.get('event_type', 'Garba & Navratri')
    event_date_str = request.POST.get('event_date', None)
    location = request.POST.get('location', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    if not name or not email or not phone or not message:
        return JsonResponse({'success': False, 'message': 'Please fill in all required fields (Name, Email, Phone, Message).'})

    event_date_val = None
    if event_date_str:
        try:
            event_date_val = date.fromisoformat(event_date_str)
        except ValueError:
            pass

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

    return JsonResponse({
        'success': True, 
        'message': f'Thank you {name}! Your inquiry for {event_type} has been sent successfully. We will get back to you soon!',
        'inquiry_id': inquiry.id
    })
