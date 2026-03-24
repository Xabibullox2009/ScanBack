from django.urls import path

from .views import home, public_qr


app_name = "qrhub"

urlpatterns = [
    path("", home, name="home"),
    path("u/<slug:slug>/", public_qr, name="public_qr"),
]
