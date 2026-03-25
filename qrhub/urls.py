from django.urls import path

from .views import home, public_qr, switch_language


app_name = "qrhub"

urlpatterns = [
    path("", home, name="home"),
    path("language/", switch_language, name="switch_language"),
    path("u/<slug:slug>/", public_qr, name="public_qr"),
    path("<slug:slug>/", public_qr, name="public_qr_short"),
]
 