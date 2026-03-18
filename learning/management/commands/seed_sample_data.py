"""Create sample modules and activities for initial setup."""
from django.core.management.base import BaseCommand
from learning.models import LearningModule, LearningActivity


class Command(BaseCommand):
    help = "Create sample learning modules and activities"

    def handle(self, *args, **options):
        modules_data = [
            (
                "Cognitive",
                "Basic cognitive skills and matching",
                "cognitive",
                [
                    ("Color Matching", "Match colors correctly", "easy", "color_match", 10),
                    ("Object Identification", "Identify common objects", "easy", "object_identification", 10),
                ],
            ),
            (
                "Communication",
                "Communication and expression",
                "communication",
                [
                    ("Basic Words", "Learn simple words", "easy", "", 10),
                ],
            ),
            (
                "Social",
                "Social interaction skills",
                "social",
                [
                    ("Emotions", "Recognize emotions", "medium", "", 15),
                ],
            ),
            (
                "Daily Life",
                "Daily living skills",
                "daily",
                [
                    ("Daily Routines", "Practice daily tasks", "medium", "", 15),
                ],
            ),
            (
                "Emotional",
                "Emotional recognition",
                "emotional",
                [
                    ("Feelings", "Identify feelings", "easy", "", 10),
                ],
            ),
            (
                "Sensory & Motor Skills",
                "Activities to support sensory processing and motor coordination",
                "cognitive",
                [
                    (
                        "Color Bubble Pop",
                        "Tap bubbles of a specific color to practice color recognition and visual attention.",
                        "easy",
                        "color_bubble_pop",
                        10,
                    ),
                ],
            ),
        ]
        for name, desc, cat, activities in modules_data:
            mod, _ = LearningModule.objects.get_or_create(
                name=name,
                defaults={"description": desc, "category": cat, "order": len(LearningModule.objects.all())},
            )
            for title, adesc, diff, tpl, pts in activities:
                LearningActivity.objects.get_or_create(
                    module=mod,
                    title=title,
                    defaults={
                        "description": adesc,
                        "difficulty": diff,
                        "template_name": tpl or "",
                        "reward_points": pts,
                    },
                )
        self.stdout.write(self.style.SUCCESS("Sample data created."))
