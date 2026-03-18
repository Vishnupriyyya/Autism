"""Views for authentication and role-based redirects."""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, CustomUserCreationForm


def home(request):
    """Landing page - hero page for all users."""
    return render(request, "index.html")


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login for all user roles."""
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("accounts:role_redirect")
    return render(request, "accounts/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Registration for parents/guardians."""
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("children:parent_dashboard")
    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    """Logout."""
    logout(request)
    return redirect("accounts:home")


@login_required
def role_redirect(request):
    """Redirect user to their role-specific dashboard."""
    user = request.user
    if user.is_administrator:
        return redirect("learning:admin_dashboard")
    if user.is_parent:
        return redirect("children:parent_dashboard")
    if user.is_child:
        # Child links to a ChildProfile; redirect to child profile list or first child
        from children.models import ChildProfile
        profile = ChildProfile.objects.filter(parent=user).first()
        if profile:
            return redirect("children:child_dashboard", pk=profile.pk)
        return redirect("children:parent_dashboard")
    return redirect("home")
