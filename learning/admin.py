from django.contrib import admin
from .models import LearningModule, LearningActivity, ActivityCompletion


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order", "is_active", "activity_count")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("order",)
    # Removed invalid filter_horizontal and inlines
    readonly_fields = ("activity_count",)

    def activity_count(self, obj):
        return obj.activities.count()
    activity_count.short_description = "Activities"

from .models import LearningActivity

class LearningActivityInline(admin.TabularInline):
    model = LearningActivity
    fields = ("title", "difficulty", "image", "audio_guide", "is_active")
    extra = 1
    readonly_fields = ()


@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "difficulty", "is_active", "has_media")
    list_filter = ("module", "difficulty", "is_active")
    search_fields = ("title", "module__name")
    ordering = ("module", "order")
    fieldsets = (
        ("Activity Info", {
            "fields": ("title", "module", "description", "difficulty", "template_name", "order")
        }),
        ("Media Uploads", {
            "fields": ("image", "audio_guide", "video_url"),
            "description": "Upload image, audio guide, and video content here. Supported formats: JPG/PNG for images, MP3/WAV for audio, YouTube/Vimeo URLs for video."
        }),
        ("Scoring & Status", {
            "fields": ("reward_points", "is_active")
        })
    )
    readonly_fields = ("has_media",)

    def has_media(self, obj):
        has = bool(obj.image or obj.audio_guide or obj.video_url)
        return "✅ Yes" if has else "❌ No"
    has_media.short_description = "Media Uploaded"


@admin.register(ActivityCompletion)
class ActivityCompletionAdmin(admin.ModelAdmin):
    list_display = ("child", "activity", "completed_at", "score", "reward_earned")
    list_filter = ("completed_at",)
