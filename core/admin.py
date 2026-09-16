from django.contrib import admin

# Register your models here.


from .models import ImpactProject, ImpactRecord

@admin.register(ImpactProject)
class ImpactProjectAdmin(admin.ModelAdmin):
    lsit_display =(
        "name",
        "country",
        "location",
        "impact_area",
        "status",
        "created_at",
    )

    list_filter =(
        "impact_area",
        "status",
        "country",
    )


    search_fields=(
        "name",
        "description",
        "country",
        "location",
    )

    @admin.register(ImpactRecord)
    class ImpactReecordAdmin(admin.ModelAdmin):
        list_display=(
            "project",
            "metric",
            "value",
            "unit",
            "recorded_at",
        )

        list_filter=(
            "unit",
            "recorded_at",
        )

        search_fields=(
            "metric",
            "project__name",
        )
