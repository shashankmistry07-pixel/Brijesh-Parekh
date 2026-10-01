from django.db import models

class SingerProfile(models.Model):
    name = models.CharField(max_length=100, default="Brijesh Parekh")
    tagline = models.CharField(max_length=200, default="Playback Singer & Electrifying Stage Performer")
    shows_count = models.IntegerField(default=4000, help_text="Total live shows performed")
    countries_count = models.IntegerField(default=15, help_text="Countries performed in")
    years_experience = models.IntegerField(default=20, help_text="Years of professional singing")
    bio_short = models.TextField(default="Let me introduce to a very talented, electrifying performer and sensational singer. Whether it's a wedding or concert, when he steps on the stage he sets it on fire. Playback singer in many Gujarati albums and movies with over 4000 shows in India and abroad.")
    bio_full = models.TextField(default="Brijesh Parekh is one of Gujarat's most celebrated playback singers and dynamic live performers. With over 4,000 successful shows globally across India, USA, UK, West Indies, and Africa, Brijesh Parekh creates magic on stage with high-energy Garba, soulful Lagangeet (wedding songs), nostalgic Bollywood Orchestra, and thrilling DJ nights. Known for his captivating voice, incredible vocal range, and unmatched stage command, he brings life and grandeur to every celebration.")
    phone_primary = models.CharField(max_length=30, default="+91 9574805348")
    phone_secondary = models.CharField(max_length=30, default="+91 9825000000")
    email = models.EmailField(default="brijeshparekh@gmail.com")
    address = models.CharField(max_length=255, default="Ahmedabad, Gujarat, India")
    facebook_url = models.URLField(default="https://www.facebook.com/brijeshparekhnight?mibextid=LQQJ4d")
    instagram_url = models.URLField(default="https://www.instagram.com/thebrijeshparekh?igsh=amIwamgxbjU0aDFh&utm_source=qr")
    youtube_url = models.URLField(default="https://youtube.com/@brijeshparekhofficial5953?si=E4l35MJxYiL2Pbgt")
    google_maps_url = models.URLField(default="https://maps.app.goo.gl/x4TiHEh2ehnbZqW7A?g_st=com.google.maps.preview.copy")
    hero_video_path = models.CharField(max_length=255, default="V1.MP4")

    def __str__(self):
        return self.name

class PerformanceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.CharField(max_length=255, help_text="Path relative to static folder")
    icon = models.CharField(max_length=100, default="fa-solid fa-music")
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Performance Categories"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(PerformanceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items')
    image_path = models.CharField(max_length=255, help_text="Path relative to static folder e.g. Garba/1.jpg")
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.title

class AudioTrack(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(PerformanceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    duration = models.CharField(max_length=20, default="04:30")
    audio_url = models.CharField(max_length=255, help_text="URL or static path to audio sample", default="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    cover_image = models.CharField(max_length=255, default="pics/solo3.jpg")
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ShowEvent(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Past', 'Past'),
        ('Sold Out', 'Sold Out'),
    ]
    title = models.CharField(max_length=200)
    category = models.ForeignKey(PerformanceCategory, on_delete=models.CASCADE, related_name='events')
    city_country = models.CharField(max_length=150)
    venue = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.CharField(max_length=100, default="08:00 PM Onwards")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    booking_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f"{self.title} - {self.city_country} ({self.event_date})"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    role_or_event = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    avatar = models.CharField(max_length=255, default="images/artist-1.jpg")

    def __str__(self):
        return f"{self.client_name} - {self.role_or_event}"

class BookingInquiry(models.Model):
    STATUS_CHOICES = [
        ('New', 'New Inquiry'),
        ('Contacted', 'Contacted'),
        ('Confirmed', 'Confirmed'),
        ('Closed', 'Closed'),
    ]

    EVENT_CHOICES = [
        ('Garba & Navratri', 'Garba & Navratri Festival'),
        ('Orchestra', 'Bollywood Orchestra & Live Band'),
        ('Wedding', 'Wedding Lagangeet & Sangeet'),
        ('International', 'International Tour / Show'),
        ('Corporate', 'Corporate Event & Award Show'),
        ('Other', 'Other Special Occasion'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default='Garba & Navratri')
    event_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.event_type} ({self.created_at.strftime('%d %b %Y')})"
