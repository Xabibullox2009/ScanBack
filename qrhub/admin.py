from django.contrib import admin
from django.utils.html import format_html

from .models import AssetContact

admin.site.site_header = "ScanBack boshqaruv paneli"
admin.site.site_title = "ScanBack Admin"
admin.site.index_title = "QR kontaktlarni boshqarish"


@admin.register(AssetContact)
class AssetContactAdmin(admin.ModelAdmin):
    list_display = (
        "public_code",
        "full_name",
        "asset_type",
        "asset_label",
        "phone_number",
        "is_active",
        "updated_at",
    )
    list_filter = ("asset_type", "is_active", "created_at", "updated_at")
    search_fields = ("public_code", "first_name", "last_name", "asset_label", "phone_number")
    list_editable = ("is_active",)
    ordering = ("-updated_at",)
    readonly_fields = ("public_url", "call_url", "uploaded_qr_preview", "created_at", "updated_at")
    fieldsets = (
        (
            "Ega ma'lumotlari",
            {"fields": (("first_name", "last_name"), "phone_number")},
        ),
        (
            "Buyum va QR",
            {"fields": ("asset_type", "asset_label", "public_code", "qr_code", "note", "is_active")},
        ),
        (
            "Public sahifa",
            {"fields": ("public_url", "call_url", "uploaded_qr_preview")},
        ),
        (
            "Tizim ma'lumotlari",
            {"fields": ("created_at", "updated_at")},
        ),
    )

    @admin.display(description="Egasi")
    def full_name(self, obj):
        return obj.full_name

    @admin.display(description="Public link")
    def public_url(self, obj):
        if not obj.pk:
            return "Avval obyektni saqlang, keyin public link chiqadi."

        url = obj.get_public_url()
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            url,
            url,
        )

    @admin.display(description="Qo'ng'iroq linki")
    def call_url(self, obj):
        if not obj.pk:
            return "Avval obyektni saqlang, keyin qo'ng'iroq linki chiqadi."

        url = f"{obj.get_public_url().rstrip('/')}/call/"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            url,
            url,
        )

    @admin.display(description="QR preview")
    def uploaded_qr_preview(self, obj):
        if not obj.pk:
            return "QR preview ko'rish uchun avval saqlang."

        if not obj.qr_code:
            return "QR rasmi hali yuklanmagan."

        return format_html(
            '<img src="{}" '
            'width="180" height="180" alt="QR preview" '
            'style="object-fit:cover;background:#fff;padding:10px;border-radius:18px;border:1px solid #d6ddcc;" />',
            obj.qr_code.url,
        )
