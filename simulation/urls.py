from . import views
from django.urls import path,include

app_name = 'simulation' 

urlpatterns = [
    path("", views.simulation_form, name="simulation_form"),
    path("result/", views.simulation_result, name="simulation_result"),
]