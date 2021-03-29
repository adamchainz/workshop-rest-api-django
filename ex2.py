import math
import os
import sys
from http import HTTPStatus

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_GET

# Configure Django

settings.configure(
    # Use Django's debug mode when the environment asks for it:
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    # Tell Django to read URL's from this module:
    ROOT_URLCONF=__name__,
    # We aren't using any security features but Django requires this setting:
    SECRET_KEY=get_random_string(50),
    # Add some useful defaults:
    MIDDLEWARE=["django.middleware.common.CommonMiddleware"],
)


# Our view functions


@require_GET
def index_view(request):
    return HttpResponse(
        "<h1>Welcome to Our Example</h1>"
        + '<p>See <a href="/api/">/api/</a> for the API.</p>'
    )


@require_GET
def api_index_view(request):
    return JsonResponse(
        data={
            "endpoints": [
                "/api/circle-area/",
            ],
        },
    )


@require_GET
def circle_area_view(request):
    errors = []

    try:
        radius = float(request.GET["radius"])
    except (KeyError, ValueError):
        errors.append("Query parameter 'radius' must be provided as a number.")

    if errors:
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={"errors": errors},
        )

    area = calculate_circle_area(radius)

    return JsonResponse(data={"area": area})


def calculate_circle_area(radius):
    return math.pi * (radius ** 2)


# Our URL configuration


urlpatterns = [
    path("", index_view),
    path("api/", api_index_view),
    path("api/circle-area/", circle_area_view),
]

# Create a WSGI application so a web server could run this for us:
app = get_wsgi_application()

# Allow running Django's commands through this file:
if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
