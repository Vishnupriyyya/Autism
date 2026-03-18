"""Views for learning modules, activities, and admin management."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from .models import LearningModule, LearningActivity, ActivityCompletion
from accounts.decorators import admin_required
from children.models import ChildProfile


# --- Administrator views ---

from accounts.models import User
from learning.models import ActivityCompletion


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with system statistics and lists for UI widgets."""
    total_users = User.objects.count()
    active_accounts = User.objects.filter(is_active=True).count()
    completions = ActivityCompletion.objects.count()
    # calculate completion rate as completions per active account (%)
    completion_rate = 0
    if active_accounts > 0:
        completion_rate = int((completions / active_accounts) * 100)

    # additional data for expanded widgets
    modules = LearningModule.objects.all()
    parents = User.objects.filter(role=User.Role.PARENT).order_by('-date_joined')[:20]
    # fetch a few child profiles to show under parents
    children = ChildProfile.objects.select_related('parent').all()[:20]

    # simple placeholder for activity trend (e.g. last 7 days)
    activity_trends = []
    # group completions by day
    from django.db.models.functions import TruncDay
    from django.db.models import Count

    trends = (
        ActivityCompletion.objects.annotate(day=TruncDay('completed_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    activity_trends = []
    for t in trends:
        activity_trends.append({
            'day': t['day'].strftime('%Y-%m-%d'),
            'count': t['count'],
            'height': t['count'] * 10,  # pixel multiplier
        })

    context = {
        'total_users': total_users,
        'active_accounts': active_accounts,
        'completions': completions,
        'completion_rate': completion_rate,
        'modules': modules,
        'parent_list': parents,
        'child_list': children,
        'activity_trends': activity_trends,
        # sidebar highlighting
        'active_section': 'dashboard',
    }
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def admin_parent_child(request):
    """View for the sidebar "Parent & Child" section of admin dashboard."""
    parents = User.objects.filter(role=User.Role.PARENT).order_by('-date_joined')
    children = ChildProfile.objects.select_related('parent').all()
    context = {
        'parent_list': parents,
        'child_list': children,
        'active_section': 'parent_child',
    }
    return render(request, 'admin/parent_child.html', context)


@admin_required
def manage_modules(request):
    """Manage learning modules and content."""
    modules = LearningModule.objects.prefetch_related("activities").all()
    return render(request, "admin/manage_modules.html", {"modules": modules})


@admin_required
def view_reports(request):
    """System-level usage statistics."""
    completions = ActivityCompletion.objects.select_related(
        "child", "activity", "child__parent"
    ).order_by("-completed_at")[:100]
    return render(request, "admin/view_reports.html", {"completions": completions})


@admin_required
def admin_settings(request):
    """Admin settings page for system configuration."""
    total_users = User.objects.count()
    total_activities = LearningActivity.objects.count()
    total_modules = LearningModule.objects.count()
    
    context = {
        'total_users': total_users,
        'total_activities': total_activities,
        'total_modules': total_modules,
        'active_section': 'settings',
    }
    return render(request, 'admin/settings.html', context)


# --- Child/Learning activity views ---

@login_required
def activity_detail(request, pk):
    """View and run a learning activity."""
    activity = get_object_or_404(LearningActivity, pk=pk, is_active=True)
    child_pk = request.GET.get("child")
    child = get_object_or_404(ChildProfile, pk=child_pk) if child_pk else None

    # Verify access: parent viewing for their child
    if child and request.user.is_parent and child.parent != request.user:
        return redirect("accounts:role_redirect")

    tpl = activity.template_name or "generic_activity.html"
    if "/" not in tpl:
        tpl = f"learning/{tpl}"
    # Ensure we have a .html extension
    if not tpl.endswith(".html"):
        tpl = f"{tpl}.html"
    template = tpl
    return render(
        request,
        template,
        {"activity": activity, "child": child},
    )


@login_required
def complete_activity(request):
    """Record activity completion (called via POST from activity page)."""
    if request.method != "POST":
        # If accessed directly by GET, show a generic completed page with no context
        return render(request, "learning/activity_completed.html", {"activity": None, "child": None})

    activity_id = request.POST.get("activity_id")
    child_id = request.POST.get("child_id")
    score = request.POST.get("score")
    reward = request.POST.get("reward", 10)

    if not activity_id or not child_id:
        return render(
            request,
            "learning/activity_completed.html",
            {"activity": None, "child": None},
        )

    activity = get_object_or_404(LearningActivity, pk=activity_id)
    child = get_object_or_404(ChildProfile, pk=child_id)

    if request.user.is_parent and child.parent != request.user:
        return redirect("accounts:role_redirect")

    ActivityCompletion.objects.create(
        child=child,
        activity=activity,
        score=int(score) if score else None,
        reward_earned=int(reward) if reward else activity.reward_points,
    )

    # Mark assignment completed if exists
    from children.models import ActivityAssignment
    from django.utils import timezone
    ActivityAssignment.objects.filter(
        child=child, activity=activity, is_completed=False
    ).update(is_completed=True, completed_at=timezone.now())

    # Show a friendly completion page instead of JSON
    return render(
        request,
        "learning/activity_completed.html",
        {"activity": activity, "child": child},
    )


def module_list(request):
    """List all learning modules (for parent/child selection)."""
    modules = LearningModule.objects.filter(is_active=True).prefetch_related("activities")
    return render(request, "learning/module_list.html", {"modules": modules})
