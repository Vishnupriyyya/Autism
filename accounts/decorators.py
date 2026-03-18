"""Role-based access decorators."""

from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def role_required(*roles):
    """Restrict view to specific user roles."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                return redirect("accounts:role_redirect")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


admin_required = role_required("admin")
parent_required = role_required("parent")
child_required = role_required("child")
