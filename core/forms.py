from django import forms
from .models import ImpactProject


class ImpactProjectForm(forms.ModelForm):

    class Meta:
        model = ImpactProject
        fields = [
            "name",
            "description",
            "country",
            "location",
            "impact_area",
            "status",
        ]


        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Describe the project and its impact...",
                    "rows": 6,
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g. North-West Region",
                }
            ),
        }
