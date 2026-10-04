from django.test import TestCase, Client
from django.urls import reverse
from .models import SingerProfile, PerformanceCategory, GalleryItem

class SingerAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = SingerProfile.objects.create(
            name="Brijesh Parekh",
            phone_primary="+91 95748 05348",
            email="brijesh71090parekh@gmail.com"
        )
        self.category = PerformanceCategory.objects.create(
            name="Garba",
            slug="garba",
            subtitle="Wedding Garba & Raas Beats",
            description="High energy Garba and marriage celebration",
            cover_image="pics/solo3.jpg",
            icon="fa-solid fa-drum",
            display_order=1
        )

    def test_pages_render_successfully(self):
        urls = [
            'home',
            'about',
            'services',
            'gallery',
            'music',
            'events',
            'contact',
        ]
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, f"Failed on {url_name}")

    def test_category_detail_view(self):
        response = self.client.get(reverse('category_detail', kwargs={'slug': 'garba'}))
        self.assertEqual(response.status_code, 200)

    def test_ajax_inquiry_submission(self):
        response = self.client.post(reverse('submit_inquiry_ajax'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+919999999999',
            'event_type': 'Garba',
            'message': 'Test booking inquiry message'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('success'))

    def test_seo_endpoints(self):
        robots_res = self.client.get(reverse('robots_txt'))
        self.assertEqual(robots_res.status_code, 200)
        self.assertIn(b"https://brijesh-parekh.vercel.app/sitemap.xml", robots_res.content)

        sitemap_res = self.client.get(reverse('sitemap_xml'))
        self.assertEqual(sitemap_res.status_code, 200)
        self.assertIn(b"https://brijesh-parekh.vercel.app/", sitemap_res.content)
        self.assertIn(b"https://brijesh-parekh.vercel.app/events/", sitemap_res.content)
