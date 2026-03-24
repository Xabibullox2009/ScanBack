from django.urls import path

from .views import AssetContactCallRedirectView, AssetContactDetailView, HomeView

app_name = "qrhub"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("scan/<slug:public_code>/", AssetContactDetailView.as_view(), name="asset-detail"),
    path("scan/<slug:public_code>/call/", AssetContactCallRedirectView.as_view(), name="asset-call"),
    path("<slug:public_code>/", AssetContactDetailView.as_view(), name="asset-detail-short"),
    path("<slug:public_code>/call/", AssetContactCallRedirectView.as_view(), name="asset-call-short"),
]
