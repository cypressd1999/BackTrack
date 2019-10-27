from django.urls import path
from . import views


urlpatterns = [
    path("", views.addpbi, name="addpbi"),
]