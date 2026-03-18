from django.contrib import admin
from .models import LearningModule, LearningActivity, ActivityCompletion


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order", "is_active")
    list_filter = ("category", "is_active")
    ordering = ("order",)


@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "difficulty", "order", "is_active")
    list_filter = ("module", "difficulty", "is_active")
    ordering = ("module", "order")


@admin.register(ActivityCompletion)
class ActivityCompletionAdmin(admin.ModelAdmin):
    list_display = ("child", "activity", "completed_at", "score", "reward_earned")
    list_filter = ("completed_at",)
