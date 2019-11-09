from django.urls import path
from . import views

app_name = 'backtrack'
urlpatterns = [
    path("<project_name>/addpbi", views.addPBI, name="addPBI"),
    path("create_project", views.createProject, name="create project"),
    path("<project_name>/deletepbi", views.deletePBI, name="delete pbi"),
    path("<project_name>/create_sb", views.createSB.as_view(), name="create sb"),
    path("<project_name>/add_task", views.addTask.as_view(), name="add sb"),
    path("<project_name>/view_pb", views.PBIView.as_view(), name="view pb")
]