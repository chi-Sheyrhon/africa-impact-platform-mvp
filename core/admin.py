from django.contrib import admin

from .models import ImpactProject, ImpactRecord


@admin.register(ImpactProject)
class ImpactProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "impact_area",
        "status",
        "start_date",
        "source_organization",
    )

    list_filter = (
        "country",
        "impact_area",
        "status",
        "source_organization",
    )

    search_fields = (
        "name",
        "description",
        "location",
        "source_organization",
        "external_project_id",
    )


@admin.register(ImpactRecord)
class ImpactRecordAdmin(admin.ModelAdmin):
    list_display = (
        "metric",
        "project",
        "category",
        "value",
        "unit",
        "recorded_at",
    )

    list_filter = (
        "category",
        "recorded_at",
    )

    search_fields = (
        "metric",
        "project__name",
    )