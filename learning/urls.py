from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/modules/", views.manage_modules, name="manage_modules"),
    path("admin/reports/", views.view_reports, name="view_reports"),
    path("admin/parent-child/", views.admin_parent_child, name="admin_parent_child"),
    path("admin/settings/", views.admin_settings, name="admin_settings"),
    path("modules/", views.module_list, name="module_list"),
    path("activity/<int:pk>/", views.activity_detail, name="activity_detail"),
    path("complete/", views.complete_activity, name="complete_activity"),
    path("shape-match/", views.shape_match_view, name="shape_match"),
]
