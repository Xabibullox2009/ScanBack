import re

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class AssetContact(models.Model):
    class AssetType(models.TextChoices):
        CAR = "car", "Mashina"
        PHONE = "phone", "Telefon"
        PASSPORT = "passport", "Passport"
        DOCUMENT = "document", "Hujjat"
        OTHER = "other", "Boshqa"

    first_name = models.CharField("Ism", max_length=120)
    last_name = models.CharField("Familiya", max_length=120)
    phone_number = models.CharField(
        "Telefon raqami",
        max_length=32,
        validators=[
            RegexValidator(
                regex=r"^[\d\+\-\(\)\s]+$",
                message="Telefon formatini to'g'ri kiriting.",
            )
        ],
        help_text="Masalan: +998 90 123 45 67",
    )
    asset_type = models.CharField(
        "Buyum turi",
        max_length=20,
        choices=AssetType.choices,
        default=AssetType.CAR,
    )
    asset_label = models.CharField(
        "Identifikator",
        max_length=180,
        help_text="Mashina nomeri, telefon modeli, passport seriyasi va hokazo.",
    )
    qr_code = models.ImageField(
        "QR code rasmi",
        upload_to="qr_codes/",
        blank=True,
        null=True,
        help_text="Admin paneldan QR rasmni yuklang.",
    )
    public_code = models.SlugField(
        "Public kod",
        max_length=80,
        unique=True,
        blank=True,
        help_text="QR scan qilinganda URL ichida ishlatiladigan noyob kod.",
    )
    note = models.TextField(
        "Qo'shimcha izoh",
        blank=True,
        help_text="Topib olgan odam ko'rishi kerak bo'lgan qisqa izoh.",
    )
    is_active = models.BooleanField(
        "Faol",
        default=True,
        help_text="Faollik o'chirilsa public sahifa ishlamaydi.",
    )
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan vaqt", auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "QR kontakt"
        verbose_name_plural = "QR kontaktlar"

    def __str__(self):
        return f"{self.full_name} - {self.asset_label}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def phone_link(self):
        return re.sub(r"[^\d+]", "", self.phone_number)

    def get_absolute_url(self):
        return reverse("qrhub:asset-detail", kwargs={"public_code": self.public_code})

    def get_public_url(self):
        base_url = getattr(settings, "SCANBACK_PUBLIC_BASE_URL", "").rstrip("/")
        path = self.get_absolute_url()
        return f"{base_url}{path}" if base_url else path

    def save(self, *args, **kwargs):
        if not self.public_code:
            self.public_code = self._generate_unique_public_code()
        super().save(*args, **kwargs)

    def _generate_unique_public_code(self):
        base = slugify(f"{self.first_name}-{self.last_name}-{self.asset_label}")[:60]
        base = base or "scanback-item"
        candidate = base
        counter = 2

        while AssetContact.objects.exclude(pk=self.pk).filter(public_code=candidate).exists():
            suffix = f"-{counter}"
            candidate = f"{base[: 80 - len(suffix)]}{suffix}"
            counter += 1

        return candidate
