from django.contrib import admin
from django.utils.html import format_html

from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "slug", "qr_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "slug")
    readonly_fields = ("slug", "qr_preview", "created_at")
    fieldsets = (
        ("Ma'lumotlar", {"fields": ("name", "phone")}),
        ("Tizim", {"fields": ("slug", "qr_image", "qr_preview", "created_at")}),
    )

    @admin.display(description="QR Kod", ordering="qr_image")
    def qr_preview(self, obj):
        if obj.qr_image:
            return format_html(
                '<img src="{}" width="120" height="120" style="border-radius:12px; object-fit:cover;" />',
                obj.qr_image.url,
            )
        return "Hali yaratilmagan"
