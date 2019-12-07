from django.urls import path
from . import views

app_name = 'backtrack'
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
	path('homepage/', views.IndexView.as_view(), name='index'),
    path("<project_name>/addpbi", views.AddPBI.as_view(), name="add pbi"),
    path("create_project", views.CreateProject.as_view(), name="create project"),
    path("<project_name>/deletepbi", views.deletePBI, name="delete pbi"),
    path("<project_name>/create_sb", views.CreateSB.as_view(), name="create sb"),
    path("<int:pk>/start_sprint", views.StartSprint.as_view(), name="start sprint"),
    path("<int:pk>/add_pbi_to_sb", views.AddPBItoSB.as_view(), name="add pbi to sb"),
    path("<int:pk>/delete_pbi_from_sb", views.DeletePBIFromSB.as_view(), name="delete pbi from sb"),
    path("<int:pk>/end_sprint", views.EndSprint.as_view(), name="end sprint"),
    path("<project_name>/add_task", views.AddTask.as_view(), name="add task"),
    path("<project_name>/view_pb", views.PBView.as_view(), name="view pb"),
    path("<project_name>/view_pb_partial", views.PBView_partial.as_view(), name="showPartialView"),  
    path("<project_name>/view_sb", views.SBView.as_view(), name="view sb"),
    path("<int:pk>/view_task", views.TaskView.as_view(), name="view task"),
    path("<int:pk>/update_task", views.UpdateTask.as_view(), name="update task"),
    path("change_contrib/", views.ajax_change_contrib, name="change contrib"),
    path("<int:pk>/view_pbi", views.ViewPBI.as_view(), name="view pbi"),
    path("<int:pk>/modify_pbi",views.ModifyPBI.as_view(), name="modify pbi"),
    path("<int:pk>/add_confirmation", views.AddConfirmation.as_view(), name="add confirmation"),
]
