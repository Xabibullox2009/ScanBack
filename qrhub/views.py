from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, TemplateView

from .models import AssetContact


class HomeView(TemplateView):
    template_name = "qrhub/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_contacts"] = AssetContact.objects.filter(is_active=True).count()
        return context


class AssetContactDetailView(DetailView):
    template_name = "qrhub/asset_detail.html"
    context_object_name = "asset"
    slug_field = "public_code"
    slug_url_kwarg = "public_code"

    def get_queryset(self):
        return AssetContact.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return render(request, "qrhub/not_found.html", status=404)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AssetContactCallRedirectView(View):
    def get(self, request, public_code, *args, **kwargs):
        try:
            asset = AssetContact.objects.get(public_code=public_code, is_active=True)
        except AssetContact.DoesNotExist:
            return render(request, "qrhub/not_found.html", status=404)

        return HttpResponse(status=302, headers={"Location": f"tel:{asset.phone_link}"})
