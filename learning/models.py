"""
Learning modules and activities for the Autism Learning Platform.
Content can be stored locally or on GCP Cloud Storage.
"""

from django.db import models


class LearningModule(models.Model):
    """A learning module (e.g. Communication, Cognitive, Social)."""

    class SkillCategory(models.TextChoices):
        COMMUNICATION = "communication", "Communication"
        SOCIAL = "social", "Social Skills"
        COGNITIVE = "cognitive", "Cognitive"
        DAILY = "daily", "Daily Life Skills"
        EMOTIONAL = "emotional", "Emotional Recognition"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=SkillCategory.choices,
        default=SkillCategory.COGNITIVE,
    )
    icon = models.ImageField(upload_to="module_icons/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class LearningActivity(models.Model):
    """A single learning activity within a module."""

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    module = models.ForeignKey(
        LearningModule,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    image = models.ImageField(upload_to="activity_images/", blank=True, null=True)
    audio_guide = models.FileField(
        upload_to="activity_audio/",
        blank=True,
        null=True,
        help_text="Audio guidance for the activity",
    )
    video_url = models.URLField(blank=True, null=True)
    template_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Template to render (e.g. color_match, object_identification)",
    )
    order = models.PositiveIntegerField(default=0)
    reward_points = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["module", "order", "title"]
        verbose_name_plural = "Learning activities"

    def __str__(self):
        return f"{self.module.name}: {self.title}"


class ActivityCompletion(models.Model):
    """Tracks when a child completes an activity (for progress and recommendations)."""

    child = models.ForeignKey(
        "children.ChildProfile",
        on_delete=models.CASCADE,
        related_name="completions",
    )
    activity = models.ForeignKey(
        LearningActivity,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    reward_earned = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-completed_at"]
        # Multiple completions allowed for repetition-based learning

    def __str__(self):
        return f"{self.child} completed {self.activity}"
