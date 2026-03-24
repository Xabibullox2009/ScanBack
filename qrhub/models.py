import uuid
from django.db import models


class QRCode(models.Model):
    name = models.CharField("Ism", max_length=100)
    phone = models.CharField("Telefon raqami", max_length=20)
    slug = models.SlugField("Slug", unique=True, blank=True)
    qr_image = models.ImageField("QR rasmi", upload_to="qr_codes/", blank=True)
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
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/u/{self.slug}/"
