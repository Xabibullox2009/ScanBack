from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import path, reverse
from django.utils.html import format_html

from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "slug", "public_url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "slug")
    readonly_fields = ("slug", "created_at", "qr_preview", "download_qr", "public_url")
    fields = ("name", "phone", "slug", "public_url", "qr_image", "qr_preview", "download_qr", "created_at")

    def get_urls(self):
        custom_urls = [
            path(
                "<path:object_id>/qr-preview/",
                self.admin_site.admin_view(self.qr_preview_view),
                name="qrhub_qrcode_qr_preview",
            ),
            path(
                "<path:object_id>/qr-download/",
                self.admin_site.admin_view(self.qr_download_view),
                name="qrhub_qrcode_qr_download",
            ),
        ]
        return custom_urls + super().get_urls()

    def _build_qr_file_response(self, request, object_id, as_attachment):
        qr_code = self.get_object(request, object_id)
        if qr_code is None or not qr_code.qr_image:
            raise Http404("QR code image not found.")

        qr_code.qr_image.open("rb")
        filename = f"{qr_code.slug or qr_code.pk}.png"
        return FileResponse(
            qr_code.qr_image,
            as_attachment=as_attachment,
            filename=filename,
            content_type="image/png",
        )

    def qr_preview_view(self, request, object_id):
        return self._build_qr_file_response(request, object_id, as_attachment=False)

    def qr_download_view(self, request, object_id):
        return self._build_qr_file_response(request, object_id, as_attachment=True)

    @admin.display(description="Public URL")
    def public_url(self, obj):
        if not obj.pk:
            return "Saved after creation"
        url = obj.get_public_url()
        return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', url, url)

    @admin.display(description="QR Preview")
    def qr_preview(self, obj):
        if not obj.pk or not obj.qr_image:
            return "QR image will appear after saving."
        preview_url = reverse("admin:qrhub_qrcode_qr_preview", args=[obj.pk])
        return format_html(
            '<img src="{}" alt="QR code for {}" style="width: 150px; height: 150px; border-radius: 12px; border: 1px solid #dbe2ea;" />',
            preview_url,
            obj.name,
        )

    @admin.display(description="Download")
    def download_qr(self, obj):
        if not obj.pk or not obj.qr_image:
            return "-"
        download_url = reverse("admin:qrhub_qrcode_qr_download", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" download>Download QR</a>',
            download_url,
        )
