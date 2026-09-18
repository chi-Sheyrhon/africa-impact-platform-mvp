from django import forms

from .models import ImpactProject, ImpactRecord


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
                    "placeholder": "Enter project name",
                }
            ),

            "description": forms.Textarea(
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


class ImpactRecordForm(forms.ModelForm):

    class Meta:
        model = ImpactRecord

        fields = [
            "metric",
            "category",
            "value",
            "unit",
            "recorded_at",
        ]

        widgets = {
            "metric": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Students reached",
                }
            ),

            "value": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 500",
                    "step": "any",
                }
            ),

            "unit": forms.TextInput(
                attrs={
                    "placeholder": "e.g. students",
                }
            ),

            "recorded_at": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }