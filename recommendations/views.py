"""Views for the recommendation engine (used by parent/child dashboards)."""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

from children.models import ChildProfile
from accounts.decorators import parent_required
from .engine import RecommendationEngine


@parent_required
@login_required
def get_recommendations(request, child_pk):
    '''API: Get recommended activities for a child.'''

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


@parent_required
@login_required
def suggestions(request):
    '''Display personalized suggestions for parent's children.'''

    children = ChildProfile.objects.filter(parent=request.user)
    recommendations_data = []
    for child in children:
        try:
            engine = RecommendationEngine(child)
            recs = engine.get_recommendations(limit=5)
            recommendations_data.append({
                'child': child,
                'recommendations': [
                    {
                        'id': a.id,
                        'title': a.title,
                        'module': getattr(a.module, 'name', 'General'),
                        'difficulty': a.difficulty,
                    } for a in recs
                ]
            })
        except Exception as e:
            logger.error(f"Error generating recs for child {child.id}: {str(e)}", exc_info=True)
            recommendations_data.append({
                'child': child,
                'recommendations': []
            })
    return render(request, 'recommendations/suggestions.html', {
        'recommendations_data': recommendations_data,
    })

