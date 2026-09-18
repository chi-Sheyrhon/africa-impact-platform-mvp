from django.urls import path
from . import views



urlpatterns = [
    path("", views.home, name="home"),

    path(
        "projects/",
        views.project_list,
        name="project_list",
    ),

    path(
        "projects/submit/",
        views.submit_project,
        name="submit_project",
    ),

    path(
        "projects/<int:project_id>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
        "projects/<int:project_id>/impact/add/",
        views.add_impact_record,
        name="add_impact_record",
    ),

    path(
        "analytics/",
        views.analytics,
        name="analytics",
    ),
]