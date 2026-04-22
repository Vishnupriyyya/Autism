from django.core.management.base import BaseCommand
from learning.models import LearningModule, LearningActivity

class Command(BaseCommand):
    help = 'Seed all learning activities from existing templates'

    def handle(self, *args, **options):
        modules_data = {
            'Cognitive': {
                'category': 'cognitive',
                'activities': [
                    {'title': 'Shape Match', 'template_name': 'shape_match', 'difficulty': 'easy'},
                    {'title': 'Size Comparison', 'template_name': 'size_comparison', 'difficulty': 'easy'},
                    {'title': 'Object Sorting', 'template_name': 'object_sorting', 'difficulty': 'medium'},
                    {'title': 'Pattern Recognition', 'template_name': 'pattern_recognition', 'difficulty': 'medium'},
                ]
            },
            'Communication': {
                'category': 'communication',
                'activities': [
                    {'title': 'Basic Words Match', 'template_name': 'basic_words_match', 'difficulty': 'easy'},
                    {'title': 'Picture Word Matching', 'template_name': 'matching_game', 'difficulty': 'medium'},
                ]
            },
            'Daily Life': {
                'category': 'daily',
                'activities': [
                    {'title': 'Brushing Teeth Routine', 'template_name': 'brushing_teeth', 'difficulty': 'easy'},
                    {'title': 'Daily Routines', 'template_name': 'daily_routines', 'difficulty': 'medium'},
                ]
            },
            'Emotional Recognition': {
                'category': 'emotional',
                'activities': [
                    {'title': 'Emotion Activity', 'template_name': 'emotion_activity', 'difficulty': 'easy'},
                    {'title': 'Feelings Match', 'template_name': 'feelings_match', 'difficulty': 'easy'},
                ]
            },
            'Social Skills': {
                'category': 'social',
                'activities': [
                    {'title': 'Social Interactions', 'template_name': 'social_interactions', 'difficulty': 'medium'},
                ]
            },
            'Sensory Motor': {
                'category': 'cognitive',
                'activities': [
                    {'title': 'Color Bubble Pop', 'template_name': 'color_bubble_pop', 'difficulty': 'easy'},
                    {'title': 'Object Identification', 'template_name': 'object_identification', 'difficulty': 'easy'},
                    {'title': 'Color Match', 'template_name': 'color_match', 'difficulty': 'easy'},
                ]
            },
        }

        created = 0
        for mod_name, data in modules_data.items():
            module, created_mod = LearningModule.objects.get_or_create(
                name=mod_name,
                defaults={'category': data['category']}
            )
            if created_mod:
                self.stdout.write(self.style.SUCCESS(f'Created module: {mod_name}'))
            
            for act_data in data['activities']:
                activity, created_act = LearningActivity.objects.get_or_create(
                    module=module,
                    template_name=act_data['template_name'],
                    defaults={
                        'title': act_data['title'],
                        'difficulty': act_data['difficulty'],
                        'is_active': True,
                        'reward_points': 15,
                    }
                )
                if created_act:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Created {act_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} new activities! Run `python manage.py collectstatic` if needed.'))


