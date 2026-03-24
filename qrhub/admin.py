from django.contrib import admin

from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "slug", "created_at")
    search_fields = ("name", "phone", "slug")
    readonly_fields = ("slug", "qr_image", "created_at")
