from django.urls import path
from . import views
urlpatterns = [ path('',views.PB.as_view(), name='productbacklog')]