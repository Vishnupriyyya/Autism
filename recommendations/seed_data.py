"""Seed sample learning modules and activities for recommendations demo."""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autism_platform.settings')

import django
django.setup()

from learning.models import LearningModule, LearningActivity
from children.models import ChildProfile
print("Seeding sample data for recommendations...")

# Create sample modules if none exist
if not LearningModule.objects.exists():
    categories = ['communication', 'cognitive', 'social', 'daily']
    for cat in categories:
        LearningModule.objects.get_or_create(
            name=f'{cat.title()} Skills',
            category=cat,
            defaults={'description': f'Sample {cat} module', 'is_active': True}
        )
    print("Created 4 sample LearningModule")
else:
    print("LearningModule already exists")

# Create sample activities if none
if not LearningActivity.objects.exists():
    modules = LearningModule.objects.all()
    for i, module in enumerate(modules):
        for j in range(3):
            LearningActivity.objects.get_or_create(
                module=module,
                title=f'{module.name} Activity {j+1}',
                difficulty=['easy', 'medium', 'hard'][j],
                defaults={
                    'description': f'Sample activity {j+1}',
                    'is_active': True,
                    'template_name': 'generic_activity',
                    'reward_points': 10
                }
            )
    print("Created 12 sample LearningActivity")
else:
    print("LearningActivity already exists")

print("Seed complete. Now suggestions should have candidates!")

