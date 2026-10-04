from django.contrib import admin
from .models import (
    SingerProfile, PerformanceCategory, GalleryItem, 
    ShowEvent, Testimonial, BookingInquiry
)

@admin.register(SingerProfile)
class SingerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'shows_count', 'phone_primary', 'email')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'shows_count', 'countries_count', 'years_experience')
        }),
        ('Biography', {
            'fields': ('bio_short', 'bio_full')
        }),
        ('Contact Info', {
            'fields': ('phone_primary', 'phone_secondary', 'email', 'address')
        }),
        ('Social Links', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'google_maps_url')
        }),
        ('Media', {
            'fields': ('hero_video_path',)
        }),
    )

@admin.register(PerformanceCategory)
class PerformanceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'subtitle', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order',)

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_path', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'caption')

@admin.register(ShowEvent)
class ShowEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city_country', 'event_date', 'status')
    list_filter = ('status', 'category', 'event_date')
    search_fields = ('title', 'venue', 'city_country')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'role_or_event', 'rating')
    list_filter = ('rating',)

@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'event_type', 'event_date', 'location', 'status', 'is_read', 'created_at')
    list_filter = ('status', 'is_read', 'event_type', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message', 'location')
    readonly_fields = ('created_at',)
    list_editable = ('status', 'is_read')
    actions = ['mark_as_read', 'mark_as_contacted', 'mark_as_confirmed']

    @admin.action(description="Mark selected inquiries as Read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected inquiries as Contacted")
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='Contacted', is_read=True)

    @admin.action(description="Mark selected inquiries as Confirmed")
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='Confirmed', is_read=True)
