from django.urls import path
from . import views


urlpatterns = [
    path("", views.addPBI, name="addPBI"),
]