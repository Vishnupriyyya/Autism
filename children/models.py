"""
Child profiles and progress tracking for the Autism Learning Platform.
"""

from django.db import models
from django.conf import settings


class ChildProfile(models.Model):
    """Profile for a child learner linked to a parent/guardian."""

    class SkillFocus(models.TextChoices):
        COMMUNICATION = "communication", "Communication"
        SOCIAL = "social", "Social Skills"
        COGNITIVE = "cognitive", "Cognitive"
        DAILY = "daily", "Daily Life Skills"
        EMOTIONAL = "emotional", "Emotional Recognition"

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="children",
        limit_choices_to={"role": "parent"},
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    skill_focus = models.JSONField(
        default=list,
        help_text="List of focus areas, e.g. ['communication', 'cognitive']",
    )
    learning_pace = models.CharField(
        max_length=20,
        choices=[
            ("slow", "Slow"),
            ("medium", "Medium"),
            ("fast", "Fast"),
        ],
        default="medium",
    )
    avatar = models.ImageField(upload_to="child_avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def grade_level(self):
        """Placeholder grade level; update once feature exists."""
        # could later be stored in model or computed based on age
        return None

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        """Return age in years based on date_of_birth, or None if unknown."""
        if not self.date_of_birth:
            return None
        from django.utils import timezone
        today = timezone.now().date()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years

    @property
    def all_competencies_completed(self):
        """Return True if every focus area has at least one completion."""
        return all(badge.get('completed') for badge in self.competency_badges)

    @property
    def competency_badges(self):
        """Generate a list of badge dicts for the child's skill_focus areas.

        Each dict contains 'label', 'color', and 'completed' (bool). The
        completion flag is set if the child has any ActivityCompletion for a
        module matching that focus category.
        """
        # simple colour palette keyed by focus value
        colour_map = {
            'communication': '#4a90e2',
            'social': '#38a169',
            'cognitive': '#f6bb42',
            'daily': '#f39c12',
            'emotional': '#9b59b6',
        }
        badges = []
        # avoid circular import; import here
        from learning.models import ActivityCompletion
        for focus in self.skill_focus or []:
            label = dict(self.SkillFocus.choices).get(focus, focus.title())
            color = colour_map.get(focus, '#999')
            # determine a simple class name based on focus for small badges
            class_map = {
                'communication': 'blue',
                'social': 'green',
                'cognitive': 'yellow',
                'daily': 'orange',
                'emotional': 'purple',
            }
            color_class = class_map.get(focus, '')
            completed = ActivityCompletion.objects.filter(
                child=self, activity__module__category=focus
            ).exists()
            badges.append({
                'label': label,
                'color': color,
                'color_class': color_class,
                'completed': completed,
            })
        return badges


class ActivityAssignment(models.Model):
    """Parent-assigned activities for a child."""

    child = models.ForeignKey(
        ChildProfile,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    activity = models.ForeignKey(
        "learning.LearningActivity",
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activity_assignments",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["child", "activity"]
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.child} - {self.activity}"
