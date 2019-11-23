from django.urls import path
from . import views

app_name = 'backtrack'
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("<project_name>/addpbi", views.AddPBI.as_view(), name="add pbi"),
    path("create_project", views.CreateProject.as_view(), name="create project"),
    path("<project_name>/deletepbi", views.deletePBI, name="delete pbi"),
    path("<project_name>/create_sb", views.CreateSB.as_view(), name="create sb"),
    path("<project_name>/add_task", views.AddTask.as_view(), name="add task"),
    path("<project_name>/view_pb", views.PBView.as_view(), name="view pb"),
    path("<project_name>/view_sb", views.SBView.as_view(), name="view sb"),
    path("<int:pk>/view_task", views.TaskView.as_view(), name="view task"),
    path("<int:pk>/view_pbi", views.ViewPBI.as_view(), name="view pbi"),
    path("<int:pk>/modify_pbi",views.ModifyPBI.as_view(), name="modify pbi"),
    path("<int:pk>/add_confirmation", views.AddConfirmation.as_view(), name="add confirmation"),
]