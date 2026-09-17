from django.shortcuts import get_object_or_404, render
from.models import ImpactProject


def home(request):
    return render(request, "core/home.html")

def project_list(request):
    projects= ImpactProject.objects.all()
    return render(
        request,
        "core/project_list.html",
        {"projects":projects},
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        ImpactProject,
        id=project_id,
    )

    return render(
        request,
        "core/project_detail.html",
        {"project": project},
    )
