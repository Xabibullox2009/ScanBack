import secrets
import string
from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


phone_validator = RegexValidator(
    regex=r"^\+\d{7,15}$",
    message="Phone number must be in international format, for example +998901234567.",
)


def generate_unique_slug(length=8):
    alphabet = string.ascii_lowercase + string.digits
    while True:
        slug = "".join(secrets.choice(alphabet) for _ in range(length))
        if not QRCode.objects.filter(slug=slug).exists():
            return slug


class QRCode(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=16, validators=[phone_validator])
    slug = models.SlugField(unique=True, blank=True)
    qr_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def save(self, *args, **kwargs):
        self.phone = self.phone.strip()
        if not self.slug:
            self.slug = generate_unique_slug()

        qr_needs_refresh = not self.qr_image or self._slug_changed()
        super().save(*args, **kwargs)

        if qr_needs_refresh:
            self.generate_qr_image(save=True)

    def _slug_changed(self):
        if not self.pk:
            return False
        original = type(self).objects.filter(pk=self.pk).values_list("slug", flat=True).first()
        return bool(original and original != self.slug)

    def get_public_url(self, base_url=None):
        resolved_base_url = (base_url or settings.APP_BASE_URL).rstrip("/")
        return f"{resolved_base_url}{reverse('qrhub:public_qr', kwargs={'slug': self.slug})}"

    def get_phone_link(self):
        return f"tel:{self.phone}"

    def get_public_display_name(self):
        parts = [part for part in self.name.split() if part]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        initials = " ".join(f"{part[0].upper()}." for part in parts[1:] if part)
        return f"{parts[0]} {initials}".strip()

    def generate_qr_image(self, save=True, base_url=None):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=15, 
            border=4,
        )
        qr.add_data(self.get_public_url(base_url=base_url))
        qr.make(fit=True)

        image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        image.save(buffer, format="PNG", dpi=(300, 300))
        buffer.seek(0)
        filename = f"{self.slug}.png"

        self.qr_image.save(filename, ContentFile(buffer.getvalue()), save=False)
        if save:
            super().save(update_fields=["qr_image"])
