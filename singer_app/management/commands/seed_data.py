import os
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from singer_app.models import (
    SingerProfile, PerformanceCategory, GalleryItem, 
    ShowEvent, Testimonial, BookingInquiry
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
        profile.phone_primary = "+91 95748 05348"
        profile.phone_secondary = ""
        profile.email = "brijesh71090parekh@gmail.com"
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
                'name': 'Garba',
                'slug': 'garba',
                'subtitle': 'Wedding Garba, Navratri Mahotsav, Marriage Raas & Traditional Beats',
                'description': 'Experience the true spirit of Gujarat with authentic Raas-Garba beats, traditional dhol, and vibrant celebrations. High-energy rhythm and non-stop music that keeps thousands dancing with festive joy.',
                'cover_image': 'pics/solo3.jpg',
                'icon': 'fa-solid fa-drum',
                'display_order': 1,
            },
            {
                'name': 'Bollywood Live',
                'slug': 'orchestra',
                'subtitle': 'Bollywood Retro & Modern Hits, Unplugged Melodies & Live Band Concerts',
                'description': 'A grand live musical concert featuring timeless Bollywood classics, romantic retro melodies, blockbuster dance numbers, and celebrity musical evenings backed by a full live orchestra band.',
                'cover_image': 'Bollywwod Live/photos/p-12.jpg',
                'icon': 'fa-solid fa-compact-disc',
                'display_order': 2,
            },
            {
                'name': 'Wedding Songs',
                'slug': 'wedding',
                'subtitle': 'Traditional Gujarati Lagangeet, Vaidik Marriage Ritual Chants & Sangeet Sandhya',
                'description': 'Sacred Vaidik marriage chants, traditional Gujarati Lagangeet, emotional Hast Melap, Kanya Vidaai, Mandap Mahurat, and joyous wedding melodies crafted to make destination marriages deeply touching and unforgettable.',
                'cover_image': 'Vaidik Lagangeet/Photos/w3.jpg',
                'icon': 'fa-solid fa-hands-praying',
                'display_order': 3,
            },
            {
                'name': 'Spiritual Music (Bhajan)',
                'slug': 'bhajan',
                'subtitle': 'Soulful Bhajans, Devotional Sandhya, Satsang & Divine Sangeet',
                'description': 'Elevate your spiritual senses with heartfelt Bhajans, divine devotional melodies, Santvani, and peaceful Satsang musical evenings sung with pure devotion, spiritual purity, and serene harmony.',
                'cover_image': 'Bhajan/photos/p-1.jpg',
                'icon': 'fa-solid fa-om',
                'display_order': 4,
            },
        ]

        PerformanceCategory.objects.exclude(slug__in=[c['slug'] for c in cat_data]).delete()
        categories = {}
        for c in cat_data:
            cat_obj, _ = PerformanceCategory.objects.update_or_create(
                slug=c['slug'],
                defaults=c
            )
            categories[c['slug']] = cat_obj

        self.stdout.write(self.style.SUCCESS('Performance Categories verified.'))

        # 3. Unique Gallery Items & Videos
        GalleryItem.objects.all().delete()
        
        unique_gallery_items = [
            # Garba, Navratri & Marriage Photos (All from Garba & Navratri Festival/Photos/ & solo3)
            ('pics/solo3.jpg', 'High-Energy Garba Vocal Recital', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/g1.jpg', 'Grand Navratri Raas-Garba Mahotsav', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/g2.jpg', 'Navratri Garba Night Arena', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/g3.jpg', 'High-Energy Garba Vocals Live', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g4.jpg', 'Live Stage Garba Performance', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g5.jpg', 'Traditional Dhol & Raas Rhythms', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g6.jpg', 'Vibrant Garba Costumes & Dancers', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/g7.jpg', 'Marriage Garba Night Celebration', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g8.jpg', 'Navratri Special Musical Evening', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g9.jpg', 'Electrifying Stage Performance', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g10.jpg', 'Raas Ramzat Celebrations Live', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g11.jpg', 'Dandiya Raas Special Arena', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/g12.jpg', 'Thousands Dancing to Garba Beats', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g13.jpg', 'Playback Singer Brijesh Parekh Live', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g14.jpg', 'Stage Lighting & Musical Ambience', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g15.jpg', 'Grand Garba Festival Ground', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/g16.jpg', 'Authentic Gujarati Folk & Raas', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g17.jpg', 'Festive Wedding Raas Beats', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g18.jpg', 'Dynamic Stage Vocal Recital', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g19.jpg', 'Celebrity Navratri Night Live', categories['garba'], False),
            ('Garba & Navratri Festival/Photos/g20.jpg', 'Non-Stop Garba Medley Performance', categories['garba'], True),
            ('Garba & Navratri Festival/Photos/6.jpg', 'Traditional Raas Garba Troupe', categories['garba'], False),
            # Garba Videos
            ('Garba & Navratri Festival/Videos/G1.MOV', 'Navratri Raas-Garba Beats Live', categories['garba'], True),
            ('Garba & Navratri Festival/Videos/G2.MOV', 'Grand Marriage Garba Night Performance', categories['garba'], True),
            ('Garba & Navratri Festival/Videos/G3.MOV', 'Dandiya Raas High-Energy Celebration', categories['garba'], True),
            
            # Bollywood Live Photos (All from Bollywwod Live/photos/)
            ('Bollywwod Live/photos/p-12.jpg', 'Celebrity Singer Musical Night', categories['orchestra'], True),
            ('Bollywwod Live/photos/p-1.jpg', 'Bollywood Live Concert Stage', categories['orchestra'], True),
            ('Bollywwod Live/photos/p-2.jpg', 'Bollywood Night Melodies & Vocals', categories['orchestra'], True),
            ('Bollywwod Live/photos/p-3.jpg', 'Celebrity Musical Concert Gala', categories['orchestra'], True),
            ('Bollywwod Live/photos/p-4.jpg', 'Musical Band Symphony Live', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-5.jpg', 'Live Orchestra Band Setup', categories['orchestra'], True),
            ('Bollywwod Live/photos/p-6.jpg', 'Dynamic Stage Mic Performance', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-7.jpg', 'Retro Hits Musical Symphony', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-8.jpg', 'Grand Stage Lighting & Ambience', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-9.jpg', 'Brijesh Parekh Bollywood Recital', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-10.jpg', 'High-Energy Bollywood Dance Set', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-11.jpg', 'Romantic Retro Melody Evening', categories['orchestra'], False),
            ('Bollywwod Live/photos/p-13.jpg', 'Orchestra Troupe Live on Stage', categories['orchestra'], False),
            # Bollywood Live Videos
            ('Bollywwod Live/Videos/O1.MP4', 'Bollywood Live Orchestra Symphony', categories['orchestra'], True),
            ('Bollywwod Live/Videos/O2.MP4', 'Retro Bollywood Melodies Live', categories['orchestra'], True),
            ('Bollywwod Live/Videos/O3.MP4', 'Celebrity Musical Concert Gala', categories['orchestra'], True),

            # Vaidik Lagangeet Photos (from static/Vaidik Lagangeet)
            ('Vaidik Lagangeet/Photos/w3.jpg', 'Traditional Vaidik Wedding Ritual Melodies', categories['wedding'], True),
            ('Vaidik Lagangeet/Photos/w1.jpg', 'Grand Wedding Sangeet Celebration', categories['wedding'], True),
            ('Vaidik Lagangeet/Photos/w2.jpg', 'Vaidik Marriage Mandap Songs', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w4.jpg', 'Royal Wedding Musical Evening', categories['wedding'], True),
            ('Vaidik Lagangeet/Photos/w5.jpg', 'Emotional Kanya Vidaai Song', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w6.jpg', 'Ganesh Sthapana & Mandap Melodies', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w7.jpg', 'Hast Melap Sacred Chants', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w8.jpg', 'Destination Wedding Music Troupe', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w9.jpg', 'Traditional Gujarati Lagangeet Live', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w10.jpg', 'Mangal Fera & Vaidik Chants', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w11.jpg', 'Wedding Sangeet Sandhya Beats', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w12.jpg', 'Joyous Marriage Celebrations', categories['wedding'], False),
            ('Vaidik Lagangeet/Photos/w13.jpg', 'Brijesh Parekh Live Wedding Recital', categories['wedding'], False),
            ('Vaidik Lagangeet/main.jpg', 'Vaidik Lagangeet Grand Stage', categories['wedding'], True),
            ('pics/group_photo.JPG', 'Brijesh Parekh Wedding Troupe', categories['wedding'], True),
            ('pics/IMG_2481.jpg', 'Brijesh Parekh Event Portrait', categories['wedding'], False),
            # Vaidik Lagangeet Videos (5 videos including w-4.MP4 & w-5.MOV)
            ('Vaidik Lagangeet/video/w1.MOV', 'Sacred Vaidik Lagangeet & Mangal Fera', categories['wedding'], True),
            ('Vaidik Lagangeet/video/w2.MOV', 'Emotional Hast Melap & Kanya Vidaai', categories['wedding'], True),
            ('Vaidik Lagangeet/video/w3.MOV', 'Royal Wedding Sangeet Sandhya Live', categories['wedding'], True),
            ('Vaidik Lagangeet/video/w-4.MP4', 'Traditional Mandap Mahurat & Lagangeet Live', categories['wedding'], True),
            ('Vaidik Lagangeet/video/w-5.MOV', 'Grand Wedding Celebrations & Sangeet Melodies', categories['wedding'], True),

            # Spiritual Music (Bhajan) Photos (from static/Bhajan/photos)
            ('Bhajan/photos/p-1.jpg', 'Spiritual Bhajan Sandhya Devotion', categories['bhajan'], True),
            ('Bhajan/photos/p-2.jpg', 'Divine Santvani & Satsang Evening', categories['bhajan'], True),
            ('Bhajan/photos/p-3.jpg', 'Soulful Krishna Bhajan Live Recital', categories['bhajan'], True),
            ('Bhajan/photos/p-4.jpg', 'Sacred Devotional Sangeet Performance', categories['bhajan'], True),
            ('Bhajan/photos/p-5.jpg', 'Shiv Stuti & Divine Chants Sandhya', categories['bhajan'], False),
            ('Bhajan/photos/p-6.jpg', 'Devotional Harmonium & Vocals', categories['bhajan'], False),
            ('Bhajan/photos/p-7.jpg', 'Spiritual Gathering & Satsang Sangeet', categories['bhajan'], False),
            ('Bhajan/photos/p-8.jpg', 'Brijesh Parekh Bhajan Recital', categories['bhajan'], False),
            ('Bhajan/photos/p-9.jpg', 'Divine Evening Prayer & Stuti', categories['bhajan'], False),
            ('Bhajan/photos/p-10.jpg', 'Grand Bhajan Mahotsav Arena', categories['bhajan'], False),
            # Spiritual Music (Bhajan) Videos (from static/Bhajan/video)
            ('Bhajan/video/v-1.MOV', 'Soulful Krishna Bhajan & Aarti Live', categories['bhajan'], True),
            ('Bhajan/video/v-2.MOV', 'Divine Santvani & Shiv Stuti Live', categories['bhajan'], True),
            ('Bhajan/video/v-3.MOV', 'Spiritual Bhajan Sandhya Performance', categories['bhajan'], True),
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

        self.stdout.write(self.style.SUCCESS(f'Populated {len(seen_paths)} strictly unique gallery and video items.'))

        # 4. Booking Inquiries (Contact Form Submissions)
        BookingInquiry.objects.all().delete()
        today = date.today()
        inquiries = [
            {
                'name': 'Shashank Mistry',
                'email': 'shashank.mistry@example.com',
                'phone': '+91 96015 05150',
                'event_type': 'Garba',
                'event_date': today + timedelta(days=25),
                'location': 'Ahmedabad, Gujarat',
                'subject': 'Navratri Raas-Garba Mahotsav 2026 Booking',
                'message': 'We are organizing a 3-night mega Navratri Garba festival in Ahmedabad expecting 8,000+ daily participants. We would love to have Brijesh Parekh lead the vocals with full orchestra team.',
                'status': 'New',
                'is_read': False,
            },
            {
                'name': 'Aarav & Swati Shah',
                'email': 'aarav.shah@gmail.com',
                'phone': '+91 98250 12345',
                'event_type': 'Wedding Songs',
                'event_date': today + timedelta(days=45),
                'location': 'Udaipur, Rajasthan',
                'subject': 'Destination Wedding Sangeet & Lagangeet',
                'message': 'Looking for traditional Gujarati Vaidik Lagangeet, Mandap Mahurat songs, Hast Melap chants, and high-energy Sangeet Sandhya for our destination wedding in Udaipur.',
                'status': 'Contacted',
                'is_read': True,
            },
            {
                'name': 'Ketan Mehta',
                'email': 'ketan.mehta@corporategroup.com',
                'phone': '+91 99090 54321',
                'event_type': 'Bollywood Live',
                'event_date': today + timedelta(days=60),
                'location': 'Mumbai, Maharashtra',
                'subject': 'Corporate Annual Gala - Bollywood Live Concert',
                'message': 'We are hosting our annual corporate gala evening at Taj Lands End Mumbai and require a 2.5-hour live Bollywood retro & modern hits concert with live band setup.',
                'status': 'Confirmed',
                'is_read': True,
            },
            {
                'name': 'Bhavin Patel',
                'email': 'bhavin.bhajan@devotee.org',
                'phone': '+91 94280 67890',
                'event_type': 'Spiritual Music (Bhajan)',
                'event_date': today + timedelta(days=15),
                'location': 'Surat, Gujarat',
                'subject': 'Pran Pratishtha & Bhajan Sandhya',
                'message': 'Requesting Brijesh Parekh for an evening of soulful Bhajans, Santvani, and devotional melodies for our temple trust ceremony in Surat.',
                'status': 'New',
                'is_read': False,
            },
            {
                'name': 'Pooja Trivedi',
                'email': 'pooja.trivedi@eventsuk.com',
                'phone': '+44 7700 900123',
                'event_type': 'Garba',
                'event_date': today + timedelta(days=90),
                'location': 'London, United Kingdom',
                'subject': 'UK Navratri Tour 2026 Inquiry',
                'message': 'We are finalizing the artist lineup for the Wembley Arena Navratri celebrations in London. Please let us know Brijeshji’s availability and international tour dates.',
                'status': 'Contacted',
                'is_read': True,
            },
        ]
        for inq in inquiries:
            BookingInquiry.objects.create(**inq)

        self.stdout.write(self.style.SUCCESS(f'Populated {len(inquiries)} Booking Inquiries.'))

        # 5. Show Events (Navratri Tour 2026 Schedule & Past Highlights)
        ShowEvent.objects.all().delete()
        events = [
            {
                'title': '9norta Navratri Mahotsav',
                'category': categories['garba'],
                'city_country': 'Ognaj, Ahmedabad',
                'venue': '9norta Festival Grounds, Ognaj',
                'event_date': date(2026, 10, 11),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Sheri Ramzat Navratri Raas',
                'category': categories['garba'],
                'city_country': 'Sindhu Bhavan, Ahmedabad',
                'venue': 'Sheri Ramzat Arena, Sindhu Bhavan Road',
                'event_date': date(2026, 10, 12),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Safal Parisar Navratri Garba Night',
                'category': categories['garba'],
                'city_country': 'South Bopal, Ahmedabad',
                'venue': 'Safal Parisar Complex, South Bopal',
                'event_date': date(2026, 10, 13),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Satvik Navratri Mahotsav',
                'category': categories['garba'],
                'city_country': 'Mehsana, Gujarat',
                'venue': 'Satvik Navratri Ground',
                'event_date': date(2026, 10, 14),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'ISKCON Platinum Dandiya & Raas',
                'category': categories['garba'],
                'city_country': 'Bopal, Ahmedabad',
                'venue': 'ISKCON Platinum Grounds, Bopal',
                'event_date': date(2026, 10, 15),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Pavagadh Shree Mahakali Mata Temple Bhakti Sandhya',
                'category': categories['bhajan'],
                'city_country': 'Pavagadh, Gujarat',
                'venue': 'Shree Mahakali Mataji Temple Complex',
                'event_date': date(2026, 10, 16),
                'event_time': '07:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Sheri Ramzat Garba Celebration',
                'category': categories['garba'],
                'city_country': 'Sindhu Bhavan, Ahmedabad',
                'venue': 'Sheri Ramzat Arena, Sindhu Bhavan Road',
                'event_date': date(2026, 10, 17),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Safal Parisar Grand Garba Finale',
                'category': categories['garba'],
                'city_country': 'South Bopal, Ahmedabad',
                'venue': 'Safal Parisar Complex, South Bopal',
                'event_date': date(2026, 10, 18),
                'event_time': '08:00 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            {
                'title': 'Private & Corporate VIP Gala Evening',
                'category': categories['orchestra'],
                'city_country': 'Ahmedabad, Gujarat',
                'venue': 'Luxury Heritage Resort & Club',
                'event_date': date(2026, 10, 19),
                'event_time': '07:30 PM Onwards',
                'status': 'Upcoming',
                'booking_link': '/contact/'
            },
            # Past Milestone Shows
            {
                'title': 'Royal Heritage Wedding Sangeet & Lagangeet',
                'category': categories['wedding'],
                'city_country': 'Udaipur, Rajasthan',
                'venue': 'The Oberoi Udaivilas Palace',
                'event_date': date(2026, 8, 15),
                'event_time': '07:30 PM',
                'status': 'Past',
                'booking_link': ''
            },
            {
                'title': 'Bollywood Live Musical Concert & Retro Symphony',
                'category': categories['orchestra'],
                'city_country': 'Mumbai, India',
                'venue': 'NCPA Auditorium, Nariman Point',
                'event_date': date(2026, 6, 20),
                'event_time': '06:30 PM',
                'status': 'Past',
                'booking_link': ''
            },
            {
                'title': 'Devotional Bhajan Ganga Sandhya & Santvani',
                'category': categories['bhajan'],
                'city_country': 'Surat, Gujarat',
                'venue': 'Sanjeev Kumar Auditorium',
                'event_date': date(2026, 5, 10),
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
                'role_or_event': 'Destination Wedding Sangeet, Udaipur',
                'content': 'Having Brijesh Parekh for our daughter’s Sangeet and Vaidik Lagangeet was the best decision we made. His wedding songs brought tears of emotion to everyone, while his Garba set turned the night into a grand party.',
                'rating': 5,
                'avatar': 'images/artist-2.jpg'
            },
            {
                'client_name': 'Pravinbhai Bhagat',
                'role_or_event': 'Spiritual Satsang & Bhajan Samiti, Surat',
                'content': 'The divine Bhajans and Santvani sung by Brijesh Parekh created a truly serene and soulful atmosphere. Everyone in attendance was deeply moved by his spiritual singing.',
                'rating': 5,
                'avatar': 'images/artist-3.jpg'
            }
        ]
        for r in reviews:
            Testimonial.objects.create(**r)

        self.stdout.write(self.style.SUCCESS('Testimonials populated successfully!'))
