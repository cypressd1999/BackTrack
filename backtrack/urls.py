from django.urls import path
from . import views

app_name = 'backtrack'
urlpatterns = [
    path("<project_name>/addpbi", views.addPBI, name="addPBI"),
    path("create_project", views.createProject, name="create project"),
    path("<project_name>/deletepbi", views.deletePBI, name="delete pbi"),
    
]