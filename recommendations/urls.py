from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path("child/<int:child_pk>/", views.get_recommendations, name="get_recommendations"),
]
