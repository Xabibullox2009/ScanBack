from django.urls import path

from .views import AssetContactDetailView, HomeView

app_name = "qrhub"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("scan/<slug:public_code>/", AssetContactDetailView.as_view(), name="asset-detail"),
]
