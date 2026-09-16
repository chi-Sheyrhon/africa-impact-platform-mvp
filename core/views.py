from django.http import HttpResponse


def home(request):
    return HttpResponse("Africa Impact Platform is running!")
