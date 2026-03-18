from django import forms
from .models import ChildProfile


class ChildProfileForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        fields = [
            "first_name", "last_name", "date_of_birth",
            "skill_focus", "learning_pace", "avatar",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "skill_focus": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skill_focus"] = forms.MultipleChoiceField(
            choices=ChildProfile.SkillFocus.choices,
            widget=forms.CheckboxSelectMultiple,
            required=False,
            initial=self.instance.skill_focus if self.instance.pk else [],
        )

    def clean_skill_focus(self):
        data = self.cleaned_data.get("skill_focus", [])
        return list(data) if data else []
