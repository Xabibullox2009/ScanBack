from django.urls import path

from . import views

app_name = "qrhub"

urlpatterns = [
    path("u/<slug:slug>/", views.public_page, name="public"),
]
