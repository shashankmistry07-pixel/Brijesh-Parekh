from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.about_view, name='profile'),
    path('services/', views.services_view, name='services'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('music/', views.music_view, name='music'),
    path('events/', views.events_view, name='events'),
    path('contact/', views.contact_view, name='contact'),
    path('api/inquiry/', views.submit_inquiry_ajax, name='submit_inquiry_ajax'),
]
