from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ImpactProjectSerializer
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, render

from .models import ImpactProject, ImpactRecord

from .forms import ImpactProjectForm, ImpactRecordForm


def home(request):

    total_projects = ImpactProject.objects.count()

    active_projects = ImpactProject.objects.filter(
        status="active"
    ).count()

    countries_count = (
        ImpactProject.objects
        .values("country")
        .distinct()
        .count()
    )

    people_reached = (
        ImpactProject.objects
        .filter(
            impact_records__metric__iexact="Students reached"
        )
        .aggregate(
            total=Sum("impact_records__value")
        )["total"]
        or 0
    )

    featured_projects=(
        ImpactProject.objects
        .filter(status="active")
        .order_by("-created_at")[:3]
    )

    impact_area_stats=(
        ImpactProject.objects
        .values("impact_area")
        .annotate(total=Count("id"))
        .order_by("-total")
                       )

    return render(
        request,
        "core/home.html",
        {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "countries_count": countries_count,
            "people_reached": people_reached,
            "featured_projects": featured_projects,
            "impact_area_stats": impact_area_stats,
        },
    )


def project_list(request):

    projects = ImpactProject.objects.all()

    # Get search and filter values
    query = request.GET.get("q", "").strip()
    country = request.GET.get("country", "").strip()
    impact_area = request.GET.get("impact_area", "").strip()
    status = request.GET.get("status", "").strip()

    # Search
    if query:
        projects = projects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(country__icontains=query)
            | Q(location__icontains=query)
        )

    # Country filter
    if country:
        projects = projects.filter(
            country__iexact=country
        )

    # Impact area filter
    if impact_area:
        projects = projects.filter(
            impact_area=impact_area
        )

    # Status filter
    if status:
        projects = projects.filter(
            status=status
        )

    # Available countries
    countries = (
        ImpactProject.objects
        .values_list("country", flat=True)
        .distinct()
        .order_by("country")
    )

    return render(
        request,
        "core/project_list.html",
        {
            "projects": projects,
            "query": query,
            "country": country,
            "impact_area": impact_area,
            "status": status,
            "countries": countries,
            "impact_areas": ImpactProject.IMPACT_AREAS,
            "statuses": ImpactProject.STATUS_CHOICES,
        },
    )


def project_detail(request, project_id):

    project = get_object_or_404(
        ImpactProject,
        id=project_id,
    )

    return render(
        request,
        "core/project_detail.html",
        {
            "project": project,
        },
    )


def analytics(request):

    total_projects = ImpactProject.objects.count()

    active_projects = ImpactProject.objects.filter(
        status="active"
    ).count()

    countries_count = (
        ImpactProject.objects
        .values("country")
        .distinct()
        .count()
    )

    total_records = (
        ImpactProject.objects
        .aggregate(
            total=Count("impact_records")
        )["total"]
        or 0
    )

    projects_by_area = (
        ImpactProject.objects
        .values("impact_area")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    records_by_category = (
        ImpactProject.objects
        .values("impact_records__category")
        .annotate(
            total=Count("impact_records")
        )
        .order_by("-total")
    )

    impact_by_metric = (
    ImpactRecord.objects
    .values("metric", "unit")
    .annotate(
        total=Sum("value")
    )
    .order_by("-total")
)



    return render(
        request,
        "core/analytics.html",
        {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "countries_count": countries_count,
            "total_records": total_records,
            "projects_by_area": projects_by_area,
            "records_by_category": records_by_category,
            "impact_by_metric": impact_by_metric,
        },
    )

def submit_project(request):

    if request.method == "POST":

        form = ImpactProjectForm(request.POST)

        if form.is_valid():

            project = form.save()

            messages.success(
                request,
                f'"{project.name}" was submitted successfully.'
            )

            return redirect(
                "project_detail",
                project_id=project.id,
            )

    else:

        form = ImpactProjectForm()

    return render(
        request,
        "core/submit_project.html",
        {
            "form": form,
        },
    )


def add_impact_record(request, project_id):

    project = get_object_or_404(
        ImpactProject,
        id=project_id,
    )

    if request.method == "POST":

        form = ImpactRecordForm(request.POST)

        if form.is_valid():

            record = form.save(commit=False)

            record.project = project

            record.save()

            messages.success(
                request,
                f'"{record.metric}" was added successfully.'
            )

            return redirect(
                "project_detail",
                project_id=project.id,
            )

    else:

        form = ImpactRecordForm()

    return render(
        request,
        "core/add_impact_record.html",
        {
            "form": form,
            "project": project,
        },
    )

@api_view(["GET", "POST"])
def api_projects(request):
    if request.method == "GET":
        projects = ImpactProject.objects.all().order_by("-start_date")
        serializer = ImpactProjectSerializer(
            projects,
            many=True
        )
        return Response(serializer.data)

    serializer = ImpactProjectSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
def api_bulk_projects(request):

    if not isinstance(request.data, list):
        return Response(
            {
                "error": "Expected a JSON list of projects."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    created_projects = []
    updated_projects = []
    errors = []

    for index, project_data in enumerate(request.data):

        source_organization = project_data.get(
            "source_organization"
        )

        external_project_id = project_data.get(
            "external_project_id"
        )

        if not source_organization or not external_project_id:
            errors.append({
                "index": index,
                "error": (
                    "source_organization and "
                    "external_project_id are required."
                ),
            })
            continue

        existing_project = ImpactProject.objects.filter(
            source_organization=source_organization,
            external_project_id=external_project_id,
        ).first()

        if existing_project:

            serializer = ImpactProjectSerializer(
                existing_project,
                data=project_data,
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()
                updated_projects.append(
                    serializer.data
                )
            else:
                errors.append({
                    "index": index,
                    "errors": serializer.errors,
                })

        else:

            serializer = ImpactProjectSerializer(
                data=project_data
            )

            if serializer.is_valid():
                project = serializer.save()
                created_projects.append(
                    serializer.data
                )
            else:
                errors.append({
                    "index": index,
                    "errors": serializer.errors,
                })

    return Response(
        {
            "created": len(created_projects),
            "updated": len(updated_projects),
            "failed": len(errors),
            "created_projects": created_projects,
            "updated_projects": updated_projects,
            "errors": errors,
        },
        status=status.HTTP_201_CREATED,
    )