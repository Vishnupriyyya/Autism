from django.contrib import admin
from .models import ChildProfile, ActivityAssignment


@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "parent", "learning_pace", "created_at")
    list_filter = ("learning_pace",)
    search_fields = ("first_name", "last_name")


@admin.register(ActivityAssignment)
class ActivityAssignmentAdmin(admin.ModelAdmin):
    list_display = ("child", "activity", "assigned_at", "is_completed")
    list_filter = ("is_completed",)
