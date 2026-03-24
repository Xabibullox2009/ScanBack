import os
import uuid

import qrcode
from django.conf import settings
from django.db import models


def generate_qr_code(qr_instance):
    if not qr_instance.slug:
        qr_instance.slug = str(uuid.uuid4())[:8]

    base_url = getattr(settings, "SCANBACK_BASE_URL", "https://scanback.onrender.com")
    url = f"{base_url}/u/{qr_instance.slug}/"

    qr_path = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    os.makedirs(qr_path, exist_ok=True)

    img = qrcode.make(url)
    img_path = os.path.join(qr_path, f"{qr_instance.slug}.png")
    img.save(img_path)

    qr_instance.qr_image = f"qr_codes/{qr_instance.slug}.png"


class QRCode(models.Model):
    name = models.CharField("Ism", max_length=100)
    phone = models.CharField("Telefon raqami", max_length=20)
    slug = models.SlugField("Slug", unique=True, blank=True)
    qr_image = models.ImageField("QR Rasmi", upload_to="qr_codes/", blank=True, null=True)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "QR Kod"
        verbose_name_plural = "QR Kodlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())[:8]

        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new and not self.qr_image:
            generate_qr_code(self)
            super().save(update_fields=["qr_image"])

    def get_public_url(self):
        base_url = getattr(settings, "SCANBACK_BASE_URL", "https://scanback.example.com")
        return f"{base_url}/u/{self.slug}/"

    def get_tel_link(self):
        return self.phone.replace(" ", "").replace("-", "")
