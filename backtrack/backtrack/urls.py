from django.urls import path
from . import views


urlpatterns = [
    path("<project_name>/addpbi", views.addPBI, name="addPBI"),
    path("create_project", views.createProject, name="create_project"),
]