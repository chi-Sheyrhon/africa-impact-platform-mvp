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
                    "min": "0",
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

    def clean_metric(self):
        metric = self.cleaned_data["metric"].strip()

        if not metric:
            raise forms.ValidationError(
                "Metric name cannot be empty."
            )

        return " ".join(metric.split()).title()

    def clean_value(self):
        value = self.cleaned_data["value"]

        if value < 0:
            raise forms.ValidationError(
                "Impact value cannot be negative."
            )

        return value

    def clean_unit(self):
        unit = self.cleaned_data["unit"].strip()

        if not unit:
            raise forms.ValidationError(
                "Unit cannot be empty."
            )

        return " ".join(unit.split()).lower()

    

    def clean_recorded_at(self):
        recorded_at = self.cleaned_data["recorded_at"]

        from django.utils import timezone

        if recorded_at > timezone.localdate():
            raise forms.ValidationError(
                "Recorded date cannot be in the future."
            )

        return recorded_at