from django.urls import path
from . import views

app_name = "children"

urlpatterns = [
    path("parent/", views.parent_dashboard, name="parent_dashboard"),
    path("parent/child/add/", views.child_create, name="child_create"),
    path("parent/child/<int:pk>/edit/", views.child_edit, name="child_edit"),
    path("child/<int:pk>/", views.child_dashboard, name="child_dashboard"),
    path("child/<int:pk>/progress/", views.progress_report, name="progress_report"),
    path("child/<int:child_pk>/assign/", views.assign_activity, name="assign_activity"),
    path("parent/module/toggle/", views.toggle_module, name="toggle_module"),
]
