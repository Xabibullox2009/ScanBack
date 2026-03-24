import shutil
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import AssetContact


def build_qr_file(name="qr-code.png"):
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\x99c\xf8\xff\xff?"
        b"\x00\x05\xfe\x02\xfeA\xd9\xa1\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return SimpleUploadedFile(name, png_bytes, content_type="image/png")


class AssetContactModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._temp_media = Path(settings.BASE_DIR) / ".test_media_model"
        cls._temp_media.mkdir(parents=True, exist_ok=True)
        cls._override = override_settings(MEDIA_ROOT=cls._temp_media)
        cls._override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._override.disable()
        shutil.rmtree(cls._temp_media, ignore_errors=True)
        super().tearDownClass()

    def test_auto_generates_qr_code_when_blank(self):
        asset = AssetContact.objects.create(
            first_name="Ali",
            last_name="Valiyev",
            phone_number="+998901112233",
            asset_type=AssetContact.AssetType.CAR,
            asset_label="01A123BC",
            qr_code=build_qr_file(),
        )

        self.assertTrue(asset.public_code)

    def test_generated_qr_code_is_unique(self):
        first = AssetContact.objects.create(
            first_name="Ali",
            last_name="Valiyev",
            phone_number="+998901112233",
            asset_type=AssetContact.AssetType.CAR,
            asset_label="01A123BC",
            qr_code=build_qr_file("first.png"),
        )
        second = AssetContact.objects.create(
            first_name="Ali",
            last_name="Valiyev",
            phone_number="+998907778899",
            asset_type=AssetContact.AssetType.CAR,
            asset_label="01A123BC",
            qr_code=build_qr_file("second.png"),
        )

        self.assertNotEqual(first.public_code, second.public_code)


class PublicFlowTests(TestCase):
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
        self.asset = AssetContact.objects.create(
            first_name="Dilshod",
            last_name="Karimov",
            phone_number="+998901234567",
            asset_type=AssetContact.AssetType.PHONE,
            asset_label="iPhone 15 Pro",
            public_code="dilshod-iphone",
            qr_code=build_qr_file("active.png"),
            note="Iltimos topgan bo'lsangiz egasiga qo'ng'iroq qiling.",
        )
        self.inactive_asset = AssetContact.objects.create(
            first_name="Aziza",
            last_name="Rasulova",
            phone_number="+998909999999",
            asset_type=AssetContact.AssetType.PASSPORT,
            asset_label="AA1234567",
            public_code="aziza-passport",
            qr_code=build_qr_file("inactive.png"),
            is_active=False,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("qrhub:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ScanBack")

    def test_home_page_is_public_information_only(self):
        response = self.client.get(reverse("qrhub:home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Admin panelga kirish")
        self.assertNotContains(response, "<form", html=False)

    def test_active_asset_page_contains_call_link(self):
        response = self.client.get(reverse("qrhub:asset-detail", args=[self.asset.public_code]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.asset.full_name)
        self.assertContains(
            response,
            reverse("qrhub:asset-call", args=[self.asset.public_code]),
        )

    def test_call_endpoint_redirects_to_phone_dialer(self):
        response = self.client.get(reverse("qrhub:asset-call", args=[self.asset.public_code]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "tel:+998901234567")

    def test_short_public_code_route_loads_asset_page(self):
        response = self.client.get(f"/{self.asset.public_code}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.asset.full_name)

    def test_inactive_asset_returns_not_found_page(self):
        response = self.client.get(reverse("qrhub:asset-detail", args=[self.inactive_asset.public_code]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "QR kod topilmadi", status_code=404)
