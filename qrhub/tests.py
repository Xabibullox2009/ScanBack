import shutil
from pathlib import Path

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import QRCode


class QRHubPublicFlowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._temp_media = Path(settings.BASE_DIR) / ".test_media_public"
        cls._temp_media.mkdir(parents=True, exist_ok=True)
        cls._override = override_settings(MEDIA_ROOT=cls._temp_media)
        cls._override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._override.disable()
        shutil.rmtree(cls._temp_media, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.qr_code = QRCode.objects.create(
            name="Dilshod Karimov",
            phone="+998901234567",
            slug="dilshod-card",
        )

    def test_home_page_defaults_to_uzbek(self):
        response = self.client.get(reverse("qrhub:home"))
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Yo&#x27;qolgan buyumlar tezroq topiladi", content)
        self.assertIn("UZ", content)

    def test_public_page_contains_call_link(self):
        response = self.client.get(reverse("qrhub:public_qr", args=[self.qr_code.slug]))
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dilshod K.")
        self.assertNotContains(response, self.qr_code.name)
        self.assertContains(response, 'href="tel:+998901234567"', html=False)
        self.assertIn("Egasiga qo&#x27;ng&#x27;iroq qilish", content)
        self.assertNotIn(">+998901234567<", content)

    def test_short_slug_route_opens_public_page(self):
        response = self.client.get(f"/{self.qr_code.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dilshod K.")

    def test_public_url_accepts_runtime_base_url(self):
        url = self.qr_code.get_public_url(base_url="http://127.0.0.1:8000")

        self.assertEqual(url, f"http://127.0.0.1:8000/u/{self.qr_code.slug}/")

    def test_switch_language_changes_home_page_copy(self):
        response = self.client.get(
            reverse("qrhub:switch_language"),
            {"lang": "ru", "next": reverse("qrhub:home")},
        )

        self.assertRedirects(response, reverse("qrhub:home"))

        follow_up = self.client.get(reverse("qrhub:home"))
        self.assertContains(follow_up, "Потерянные вещи находятся быстрее")
        self.assertContains(follow_up, "RU")

    def test_switch_language_changes_public_page_copy(self):
        self.client.get(
            reverse("qrhub:switch_language"),
            {"lang": "en", "next": reverse("qrhub:public_qr", args=[self.qr_code.slug])},
        )

        response = self.client.get(reverse("qrhub:public_qr", args=[self.qr_code.slug]))

        self.assertContains(response, "If you found this item, please call the owner.")
        self.assertContains(response, "Call Owner")


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class AdminPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pass12345",
        )
        QRCode.objects.create(
            name="Admin Check",
            phone="+998901234567",
            slug="admin-check",
        )
        self.client.force_login(self.user)

    def test_qrcode_changelist_opens(self):
        response = self.client.get("/admin/qrhub/qrcode/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Check")
