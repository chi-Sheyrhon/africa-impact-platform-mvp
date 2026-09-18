from rest_framework import serializers

from .models import ImpactProject, ImpactRecord


class ImpactRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactRecord
        fields = [
            "id",
            "metric",
            "category",
            "value",
            "unit",
            "recorded_at",
        ]


class ImpactProjectSerializer(serializers.ModelSerializer):
    impact_records = ImpactRecordSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ImpactProject
        fields = [
            "id",
            "name",
            "description",
            "country",
            "location",
            "impact_area",
            "status",
            "start_date",
            "end_date",
            "source_organization",
            "source_url",
            "external_project_id",
            "created_at",
            "impact_records",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "impact_records",
        ]