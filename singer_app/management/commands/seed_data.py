import os
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from singer_app.models import (
    SingerProfile, PerformanceCategory, GalleryItem, 
    AudioTrack, ShowEvent, Testimonial
)

class Command(BaseCommand):
    help = 'Seed database with unique, production-ready media and categories for Singer Brijesh Parekh'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # 1. Singer Profile
        profile, created = SingerProfile.objects.get_or_create(id=1)
        profile.name = "Brijesh Parekh"
        profile.tagline = "Sensational Gujarati Playback Singer & International Live Performer"
        profile.shows_count = 4000
        profile.countries_count = 15
        profile.years_experience = 22
        profile.bio_short = (
            "Meet Brijesh Parekh — an electrifying performer and sensational playback singer. "
            "Whether it's a grand wedding or a massive stadium concert, when he steps onto the stage, he sets it on fire. "
            "Playback singer in numerous Gujarati albums and movies with over 4,000 shows across India and abroad."
        )
        profile.bio_full = (
            "Brijesh Parekh is one of Gujarat's most celebrated playback singers, composers, and dynamic live performers. "
            "With an extraordinary career spanning over 22 years and more than 4,000 successful shows globally across India, USA, UK, "
            "West Indies, and Africa, Brijesh Parekh creates musical magic on stage.\n\n"
            "His repertoire ranges from high-energy Navratri Raas-Garba festivals and traditional Vaidik Lagangeet (wedding rituals) "
            "to nostalgic Bollywood orchestra evenings, celebrity galas, and live DJ nights. "
            "Renowned for his vocal range, stage command, and genuine connection with audiences of all generations, "
            "Brijesh Parekh brings grandeur, joy, and unforgettable energy to every celebration."
        )
        profile.phone_primary = "+91 9574805348"
        profile.phone_secondary = "+91 9825000000"
        profile.email = "brijeshparekh@gmail.com"
        profile.address = "Ahmedabad, Gujarat, India"
        profile.facebook_url = "https://www.facebook.com/brijeshparekhnight?mibextid=LQQJ4d"
        profile.instagram_url = "https://www.instagram.com/thebrijeshparekh?igsh=amIwamgxbjU0aDFh&utm_source=qr"
        profile.youtube_url = "https://youtube.com/@brijeshparekhofficial5953?si=E4l35MJxYiL2Pbgt"
        profile.google_maps_url = "https://maps.app.goo.gl/x4TiHEh2ehnbZqW7A?g_st=com.google.maps.preview.copy"
        profile.hero_video_path = "V1.MP4"
        profile.save()

        self.stdout.write(self.style.SUCCESS('Singer Profile verified.'))

        # 2. Performance Categories
        cat_data = [
            {
                'name': 'Garba & Navratri Festival',
                'slug': 'garba',
                'subtitle': 'Wedding Garba, Navratri Mahotsav, Corporate Garba & Raas Ramzat',
                'description': 'Experience the true spirit of Gujarat with non-stop traditional and fusion Raas-Garba beats. High-energy rhythm, traditional dhol, and vibrant stage presence that keeps thousands dancing all night long.',
                'cover_image': 'pics/solo3.jpg',
                'icon': 'fa-solid fa-drum',
                'display_order': 1,
            },
            {
                'name': 'Orchestra & Bollywood Live',
                'slug': 'orchestra',
                'subtitle': 'Bollywood Retro & Hits, Celebrity Shows, Corporate Nights & Mimicry',
                'description': 'A grand live orchestra band performing timeless Bollywood classics, energetic dance numbers, corporate galas, and celebrity musical evenings with complete sound and lighting production.',
                'cover_image': 'pics/alb1.JPG',
                'icon': 'fa-solid fa-compact-disc',
                'display_order': 2,
            },
            {
                'name': 'Wedding Songs & Lagangeet',
                'slug': 'wedding',
                'subtitle': 'Traditional Gujarati Wedding Songs, Vaidik Ritual Songs & Sangeet Sandhya',
                'description': 'Sacred Vaidik marriage chants, emotional Hast Melap, Kanya Vidaai, Mandap Mahurat, and joyous Sangeet Sandhya melodies crafted to make destination weddings unforgettable.',
                'cover_image': 'Lagangeet/main.jpg',
                'icon': 'fa-solid fa-hands-praying',
                'display_order': 3,
            },
            {
                'name': 'International Concert Shows',
                'slug': 'international',
                'subtitle': 'USA, UK, West Indies & Africa World Concert Tours',
                'description': 'Global concert tours bringing authentic Indian music and cultural celebrations to NRI communities around the world with full orchestra and dynamic stage visuals.',
                'cover_image': 'International/main.jpg',
                'icon': 'fa-solid fa-plane-departure',
                'display_order': 4,
            },
        ]

        categories = {}
        for c in cat_data:
            cat_obj, _ = PerformanceCategory.objects.update_or_create(
                slug=c['slug'],
                defaults=c
            )
            categories[c['slug']] = cat_obj

        self.stdout.write(self.style.SUCCESS('Performance Categories verified.'))

        # 3. Unique Gallery Items (strictly no duplicates)
        GalleryItem.objects.all().delete()
        
        unique_gallery_items = [
            # Garba Category
            ('Garba/1.jpg', 'Navratri Garba Night Arena', categories['garba'], True),
            ('Garba/2.jpg', 'Navratri Festival Crowds', categories['garba'], False),
            ('Garba/3.jpg', 'Live Stage Garba Performance', categories['garba'], False),
            ('Garba/5.jpg', 'Traditional Dhol & Raas Rhythms', categories['garba'], False),
            ('Garba/6.jpg', 'Vibrant Garba Costumes & Dancers', categories['garba'], True),
            ('Garba/7.jpg', 'Corporate Garba Night Celebration', categories['garba'], False),
            ('Garba/8.jpg', 'Navratri Special Evening', categories['garba'], False),
            ('Garba/9.jpg', 'High-Energy Garba Vocals', categories['garba'], False),
            ('Garba/10.jpg', 'Raas Ramzat Celebrations', categories['garba'], False),
            ('Garba/n.jpg', 'Dandiya Raas Special Stage', categories['garba'], False),
            ('Garba/n1.jpg', 'Thousands Dancing to Garba Beats', categories['garba'], True),
            ('Garba/n2.jpg', 'Playback Singer Brijesh Parekh Live', categories['garba'], False),
            ('Garba/n3.jpg', 'Stage Lighting & Musical Ambience', categories['garba'], False),
            ('Garba/big.jpg', 'Grand Navratri Festival Ground', categories['garba'], True),
            
            # Orchestra Category
            ('Orchesra/1.jpg', 'Live Orchestra Stage Concert', categories['orchestra'], True),
            ('Orchesra/2.jpg', 'Musical Band Symphony Live', categories['orchestra'], False),
            ('Orchesra/3.jpg', 'Bollywood Night Melodies', categories['orchestra'], False),
            ('Orchesra/4.jpg', 'Corporate Award Show Gala', categories['orchestra'], True),
            ('Orchesra/5.jpg', 'Sound & Light Stage Production', categories['orchestra'], False),
            ('Orchesra/6.jpg', 'Celebrity Singer Evening', categories['orchestra'], False),
            ('Orchesra/7.jpg', 'Brijesh Parekh with Live Troupe', categories['orchestra'], False),
            ('Orchesra/8.jpg', 'Retro Hits Musical Symphony', categories['orchestra'], False),
            ('pics/poster.jpg', 'Silverstar Orchestra Official Poster', categories['orchestra'], True),

            # Wedding Category
            ('Lagangeet/main.jpg', 'Grand Wedding Sangeet Celebration', categories['wedding'], True),
            ('Lagangeet/2.jpg', 'Vaidik Marriage Mandap Songs', categories['wedding'], False),
            ('Lagangeet/3.jpg', 'Traditional Gujarati Lagangeet', categories['wedding'], False),
            ('Lagangeet/4.jpg', 'Royal Wedding Musical Evening', categories['wedding'], True),
            ('Lagangeet/5.jpg', 'Emotional Kanya Vidaai Song', categories['wedding'], False),
            ('Lagangeet/6.jpg', 'Ganesh Sthapana & Mandap Melodies', categories['wedding'], False),
            ('Lagangeet/7.jpg', 'Hast Melap Sacred Chants', categories['wedding'], False),
            ('pics/group_photo.JPG', 'Brijesh Parekh Wedding Troupe', categories['wedding'], True),

            # International Category
            ('International/main.jpg', 'USA World Tour Concert Stage', categories['international'], True),
            ('International/1.jpg', 'London UK Cultural Night', categories['international'], True),
            ('International/2.jpg', 'African Diaspora Cultural Festival', categories['international'], False),

            # Unique Portraits & Live Stage
            ('pics/solo1.JPG', 'Brijesh Parekh Studio Portrait', categories['garba'], False),
            ('pics/solo2.jpg', 'Dynamic Stage Mic Performance', categories['orchestra'], True),
            ('pics/solo4.JPG', 'Concert High-Energy Vocalist', categories['garba'], False),
            ('pics/p 1.jpg', 'Stage Performance Highlight', categories['orchestra'], False),
            ('pics/p2.jpg', 'Live Stage Vocal Moment', categories['garba'], False),
            ('pics/IMG_2481.jpg', 'Brijesh Parekh Event Portrait', categories['wedding'], False),
        ]

        seen_paths = set()
        for path, title, cat_obj, is_feat in unique_gallery_items:
            if path not in seen_paths:
                seen_paths.add(path)
                GalleryItem.objects.create(
                    title=title,
                    category=cat_obj,
                    image_path=path,
                    is_featured=is_feat
                )

        self.stdout.write(self.style.SUCCESS(f'Populated {len(seen_paths)} strictly unique gallery items.'))

        # 4. Audio Tracks
        AudioTrack.objects.all().delete()
        tracks = [
            {
                'title': 'Ranglo Non-Stop Garba Medley 2026',
                'category': categories['garba'],
                'duration': '06:45',
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'cover_image': 'pics/solo3.jpg',
                'is_popular': True,
            },
            {
                'title': 'Bollywood Unplugged Retro Symphony',
                'category': categories['orchestra'],
                'duration': '05:20',
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
                'cover_image': 'pics/alb1.JPG',
                'is_popular': True,
            },
            {
                'title': 'Vaidik Gujarati Lagangeet & Mangal Fera',
                'category': categories['wedding'],
                'duration': '07:15',
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
                'cover_image': 'Lagangeet/main.jpg',
                'is_popular': True,
            },
            {
                'title': 'Raas Ramzat Navratri Special Live',
                'category': categories['garba'],
                'duration': '08:30',
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
                'cover_image': 'Garba/n1.jpg',
                'is_popular': True,
            },
            {
                'title': 'USA International Tour Live Medley',
                'category': categories['international'],
                'duration': '05:50',
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3',
                'cover_image': 'International/main.jpg',
                'is_popular': False,
            },
            {
                'title': 'Kanya Vidaai & Mandap Melodies',
                'category': categories['wedding'],
                'duration': '04:40',
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3',
                'cover_image': 'pics/solo2.jpg',
                'is_popular': False,
            },
        ]
        for t in tracks:
            AudioTrack.objects.create(**t)

        self.stdout.write(self.style.SUCCESS('Audio Tracks populated.'))

        # 5. Show Events
        ShowEvent.objects.all().delete()
        today = date.today()
        events = [
            {
                'title': 'Grand Navratri Garba Festival 2026',
                'category': categories['garba'],
                'city_country': 'Ahmedabad, India',
                'venue': 'YMCA Club Grounds, SG Highway',
                'event_date': today + timedelta(days=14),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Royal Heritage Wedding Sangeet Sandhya',
                'category': categories['wedding'],
                'city_country': 'Udaipur, Rajasthan',
                'venue': 'The Oberoi Udaivilas Palace',
                'event_date': today + timedelta(days=28),
                'event_time': '07:30 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'USA Cultural Garba & Music Tour',
                'category': categories['international'],
                'city_country': 'New Jersey, USA',
                'venue': 'NJ Convention & Exposition Center',
                'event_date': today + timedelta(days=50),
                'event_time': '07:00 PM EST',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Bollywood Musical Orchestra & Celebrity Gala',
                'category': categories['orchestra'],
                'city_country': 'Mumbai, India',
                'venue': 'NCPA Auditorium, Nariman Point',
                'event_date': today + timedelta(days=65),
                'event_time': '06:30 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'London Raas Garba Night',
                'category': categories['international'],
                'city_country': 'London, UK',
                'venue': 'Wembley Arena',
                'event_date': today - timedelta(days=35),
                'event_time': '07:00 PM GMT',
                'status': 'Past',
                'booking_link': ''
            },
            {
                'title': 'Corporate Annual Awards Night & Live Band',
                'category': categories['orchestra'],
                'city_country': 'Bengaluru, India',
                'venue': 'The Leela Palace Ballroom',
                'event_date': today - timedelta(days=80),
                'event_time': '07:00 PM',
                'status': 'Past',
                'booking_link': ''
            },
        ]
        for e in events:
            ShowEvent.objects.create(**e)

        self.stdout.write(self.style.SUCCESS('Show Events populated.'))

        # 6. Testimonials
        Testimonial.objects.all().delete()
        reviews = [
            {
                'client_name': 'Rajesh Shah',
                'role_or_event': 'Navratri Festival Organizer, Ahmedabad',
                'content': 'Brijesh Parekh created pure magic at our Navratri ground with over 15,000 people dancing to his voice. His energy, stamina, and song selection are unmatched in the entire industry!',
                'rating': 5,
                'avatar': 'images/artist-1.jpg'
            },
            {
                'client_name': 'Meeta & Sameer Patel',
                'role_or_event': 'Destination Wedding, Udaipur',
                'content': 'Having Brijesh Parekh for our daughter’s Sangeet and Lagangeet was the best decision we made. His Vaidik wedding songs brought tears of emotion to everyone, while his Garba set turned the night into a grand party.',
                'rating': 5,
                'avatar': 'images/artist-2.jpg'
            },
            {
                'client_name': 'Devang Mehta',
                'role_or_event': 'Gujarati Cultural Association, New Jersey USA',
                'content': 'Brijesh Parekh’s USA tour was a massive hit. He made all of us feel right at home with his powerful vocals and authentic Gujarati raas-garba flavor.',
                'rating': 5,
                'avatar': 'images/artist-3.jpg'
            }
        ]
        for r in reviews:
            Testimonial.objects.create(**r)

        self.stdout.write(self.style.SUCCESS('Testimonials populated successfully!'))
