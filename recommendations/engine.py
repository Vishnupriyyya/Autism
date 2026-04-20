"""
Rule-based Recommendation Engine for the Autism Learning Platform.
Analyzes completed activities, difficulty levels, and repetition patterns
to suggest suitable learning tasks. Parents can override recommendations.
"""

from django.db.models import Count
from learning.models import LearningActivity, LearningModule, ActivityCompletion
from children.models import ChildProfile, ActivityAssignment


class RecommendationEngine:
    """
    System actor: generates activity recommendations based on child progress.
    """

    def __init__(self, child: ChildProfile):
        self.child = child
        self.skill_focus = getattr(child, 'skill_focus', []) or []
        self.learning_pace = getattr(child, 'learning_pace', 'medium')

    def get_recommendations(self, limit=5):
        """
        Generate recommended activities using rule-based logic:
        1. Prefer child's skill focus areas
        2. Consider difficulty based on recent performance
        3. Include repetition for reinforcement (previously completed)
        4. Exclude already-assigned incomplete activities
        """
        skill_focus = self.skill_focus

        # Get IDs of activities already assigned but not completed
        assigned_ids = set(
ActivityAssignment.objects.filter(
                child=self.child, is_completed=False
            ).values_list("activity_id", flat=True)
        )

        # Completed activity IDs and counts (for repetition logic)
        completed = (
ActivityCompletion.objects.filter(child=self.child)
            .values("activity_id")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        completed_ids = {c["activity_id"]: c["count"] for c in completed}

        # Base queryset: active activities not yet assigned
        candidates = (
            LearningActivity.objects.filter(is_active=True)
            .exclude(id__in=assigned_ids)
            .select_related("module")
        )

        # Score each candidate
        scored = []
        for activity in candidates:
            score = 0

            # Prefer skill focus
            if activity.module.category in skill_focus:
                score += 20

            # Difficulty: match learning pace
            if self.learning_pace == "slow" and activity.difficulty == "easy":
                score += 15
            elif self.learning_pace == "medium":
                score += 10
            elif self.learning_pace == "fast" and activity.difficulty in ("medium", "hard"):
                score += 15

            # Repetition: completed 1-2 times gets bonus (reinforcement)
            count = completed_ids.get(activity.id, 0)
            if 1 <= count <= 2:
                score += 25
            elif count == 0:
                score += 5  # New activities

            scored.append((activity, score))

        # Sort by score descending
        scored.sort(key=lambda x: -x[1])

        return [a for a, _ in scored[:limit]]

    def get_repetition_candidates(self, limit=3):
        """Activities completed 1-2 times, good for reinforcement."""
        completed_counts = (
            ActivityCompletion.objects.filter(child=self.child)
            .values("activity_id")
            .annotate(count=Count("id"))
        )
        ids = [
            c["activity_id"]
            for c in completed_counts
            if 1 <= c["count"] <= 2
        ][:limit]
        return list(LearningActivity.objects.filter(id__in=ids, is_active=True))
