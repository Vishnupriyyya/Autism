"""
User accounts and roles for the Autism Learning Platform.
Supports Administrator, Parent/Guardian, and Child (Learner) actors.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with role-based access."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        PARENT = "parent", "Parent/Guardian"
        CHILD = "child", "Child (Learner)"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PARENT)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    def get_role_display(self):
        return dict(self.Role.choices).get(self.role, self.role)

    @property
    def is_administrator(self):
        return self.role == self.Role.ADMIN

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT

    @property
    def is_child(self):
        return self.role == self.Role.CHILD
