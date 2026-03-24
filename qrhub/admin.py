from django.contrib import admin
from django.utils.html import format_html

from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "slug", "qr_preview", "download_qr", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "slug")
    readonly_fields = ("slug", "created_at", "qr_preview", "download_qr", "public_url")
    fields = ("name", "phone", "slug", "public_url", "qr_image", "qr_preview", "download_qr", "created_at")

    @admin.display(description="Public URL")
    def public_url(self, obj):
        if not obj.pk:
            return "Saved after creation"
        url = obj.get_public_url()
        return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', url, url)

    @admin.display(description="QR Preview")
    def qr_preview(self, obj):
        if not obj.qr_image:
            return "QR image will appear after saving."
        return format_html(
            '<img src="{}" alt="QR code for {}" style="width: 150px; height: 150px; border-radius: 12px; border: 1px solid #dbe2ea;" />',
            obj.qr_image.url,
            obj.name,
        )

    @admin.display(description="Download")
    def download_qr(self, obj):
        if not obj.qr_image:
            return "-"
        return format_html(
            '<a class="button" href="{}" download>Download QR</a>',
            obj.qr_image.url,
        )
