"""Views for the recommendation engine (used by parent/child dashboards)."""

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from children.models import ChildProfile
from accounts.decorators import parent_required
from .engine import RecommendationEngine


@parent_required
@login_required
def get_recommendations(request, child_pk):
    """API: Get recommended activities for a child."""
    child = get_object_or_404(ChildProfile, pk=child_pk, parent=request.user)
    engine = RecommendationEngine(child)
    activities = engine.get_recommendations(limit=5)
    return JsonResponse({
        "recommendations": [
            {
                "id": a.id,
                "title": a.title,
                "module": a.module.name,
                "difficulty": a.difficulty,
            }
            for a in activities
        ],
    })
