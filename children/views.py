"""Views for Parent and Child dashboards."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import ChildProfile, ActivityAssignment
from .forms import ChildProfileForm
from accounts.decorators import parent_required
from recommendations.engine import RecommendationEngine
from learning.models import LearningActivity


@parent_required
def parent_dashboard(request):
    """Parent dashboard: manage children, assign activities, view progress."""
    children = ChildProfile.objects.filter(parent=request.user)

    # build a simple list of modules with progress percentage based on
    # assignments for all of the parent's children
    assignments = ActivityAssignment.objects.filter(child__parent=request.user).select_related(
        "activity__module"
    )
    module_stats: dict = {}
    for a in assignments:
        mod = a.activity.module
        stats = module_stats.setdefault(mod.pk, {"name": mod.name, "total": 0, "completed": 0})
        stats["total"] += 1
        if a.is_completed:
            stats["completed"] += 1

    # load toggle state stored in session (per-parent)
    enabled_map = request.session.get("module_enabled", {})

    assigned_modules = []
    for stats in module_stats.values():
        total = stats["total"]
        completed = stats["completed"]
        progress = int(completed / total * 100) if total else 0
        enabled = enabled_map.get(stats["name"], True)
        assigned_modules.append(
            {"name": stats["name"], "progress": progress, "enabled": enabled}
        )

    # compile a skills overview for the header section
    # each focus area with a completion mark if any child has activity in that category
    skill_defs = [
        ("Cognitive", "blue", "fas fa-brain", "cognitive"),
        ("Communication", "green", "fas fa-comments", "communication"),
        ("Physical", "yellow", "fas fa-child", "daily"),
        ("Social", "orange", "fas fa-heart", "social"),
    ]
    from learning.models import ActivityCompletion
    skills_overview = []
    for label, color_class, icon, category in skill_defs:
        completed = ActivityCompletion.objects.filter(
            child__parent=request.user, activity__module__category=category
        ).exists()
        skills_overview.append({
            "label": label,
            "color_class": color_class,
            "icon": icon,
            "completed": completed,
        })

    return render(
        request,
        "parent_dashboard.html",
        {
            "children": children,
            "assigned_modules": assigned_modules,
            "skills_overview": skills_overview,
        },
    )


@parent_required

def child_create(request):
    """Create a new child profile."""
    form = ChildProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        child = form.save(commit=False)
        child.parent = request.user
        child.save()
        return redirect("children:parent_dashboard")
    return render(request, "children/child_form.html", {"form": form, "action": "Add"})


@parent_required
def child_edit(request, pk):
    """Edit child profile."""
    child = get_object_or_404(ChildProfile, pk=pk, parent=request.user)
    form = ChildProfileForm(request.POST or None, request.FILES or None, instance=child)
    if form.is_valid():
        form.save()
        return redirect("children:parent_dashboard")
    return render(request, "children/child_form.html", {"form": form, "child": child, "action": "Edit"})


@login_required
def child_dashboard(request, pk):
    """Child-friendly dashboard: assigned activities, simple layout."""
    child = get_object_or_404(ChildProfile, pk=pk)
    # Only parent can access child dashboard (or we could add PIN later)
    if not request.user.is_parent or child.parent != request.user:
        if request.user.is_administrator:
            pass  # Admin can view any
        else:
            return redirect("accounts:role_redirect")

    assignments = ActivityAssignment.objects.filter(
        child=child, is_completed=False
    ).select_related("activity", "activity__module").order_by("-assigned_at")

    # System recommendations (parent can override by assigning)
    engine = RecommendationEngine(child)
    recommended = engine.get_recommendations(limit=5)

    # All available activities (for explicit assignment)
    all_activities = (
        LearningActivity.objects.filter(is_active=True)
        .select_related("module")
        .order_by("module__name", "order", "title")
    )

    return render(
        request,
        "child_dashboard.html",
        {
            "child": child,
            "assignments": assignments,
            "recommended": recommended,
            "all_activities": all_activities,
        },
    )


@parent_required
def progress_report(request, pk):
    """Detailed progress report for a child."""
    child = get_object_or_404(ChildProfile, pk=pk, parent=request.user)
    from learning.models import ActivityCompletion
    completions = ActivityCompletion.objects.filter(
        child=child
    ).select_related("activity", "activity__module").order_by("-completed_at")
    return render(
        request,
        "parent_progress.html",
        {"child": child, "completions": completions},
    )


@parent_required

def toggle_module(request):
    """AJAX endpoint to toggle module visibility state for this parent.

    Expects POST data with 'module_name' and 'enabled' ('true'/'false').
    State is saved in the session under 'module_enabled'.
    """
    if request.method == "POST":
        name = request.POST.get("module_name")
        enabled = request.POST.get("enabled") == "true"
        if name:
            mapping = request.session.get("module_enabled", {})
            mapping[name] = enabled
            request.session["module_enabled"] = mapping
            return JsonResponse({"status": "ok", "module": name, "enabled": enabled})
    return JsonResponse({"status": "error"}, status=400)


@parent_required
def assign_modules(request):
    children = ChildProfile.objects.filter(parent=request.user).order_by('first_name')
    activities = LearningActivity.objects.filter(is_active=True).select_related('module').order_by('module__name', 'module__order', 'order')
    
    if request.method == 'POST':
        child_id = request.POST.get('child_id')
        activity_ids = request.POST.getlist('activities')
        if child_id:
            child = ChildProfile.objects.get(pk=child_id, parent=request.user)
            assigned_count = 0
            for activity_id in activity_ids:
                activity = LearningActivity.objects.get(pk=activity_id)
                ActivityAssignment.objects.get_or_create(child=child, activity=activity)
                assigned_count += 1
            messages.success(request, f'Assigned {assigned_count} activities to {child.get_full_name()}.')
        else:
            messages.error(request, 'Please select a child.')
    
    context = {'children': children, 'activities': activities}
    return render(request, 'children/assign_modules.html', context)

@parent_required
def progress_overview(request):
    children = ChildProfile.objects.filter(parent=request.user).prefetch_related('completions__activity').order_by('first_name')
    context = {'children': children}
    return render(request, 'children/progress_overview.html', context)


@parent_required
def assign_activity(request, child_pk):
    """Assign an activity to a child (parent override of recommendations)."""
    child = get_object_or_404(ChildProfile, pk=child_pk, parent=request.user)
    if request.method == "POST":
        activity_id = request.POST.get("activity_id")
        if activity_id:
            from learning.models import LearningActivity
            activity = get_object_or_404(LearningActivity, pk=activity_id)
            ActivityAssignment.objects.get_or_create(
                child=child,
                activity=activity,
                defaults={"assigned_by": request.user},
            )
        return redirect("children:child_dashboard", pk=child.pk)
    return redirect("children:child_dashboard", pk=child.pk)
