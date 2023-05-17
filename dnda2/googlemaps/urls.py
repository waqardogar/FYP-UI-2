from django.urls import path
from . import views
from pathplanning import views as v_p
urlpatterns=[
    path("",views.dashboard),
    path("pp/", v_p.pathplanning,name="pathplanning"),
]