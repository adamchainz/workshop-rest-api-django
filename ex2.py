import os
import random
import sys
from http import HTTPStatus

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse
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
def index(request):
    return JsonResponse(
        data={
            "endpoints": [
                "/api/predict-rain/",
            ],
        },
    )


@require_GET
def predict_rain(request):
    errors = []
    try:
        # In celsius
        temperature = request.GET["temperature"]
    except KeyError:
        errors.append("Query parameter 'temperature' must be provided.")
    else:
        try:
            temperature = float(temperature)
        except ValueError:
            errors.append("Query parameter 'temperature' must be a valid number.")

    if errors:
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={"errors": errors},
        )

    rain_probability = sophisticated_model_to_predict_rain(temperature)

    return JsonResponse(data={"rain_probability": rain_probability})


def sophisticated_model_to_predict_rain(temperature):
    # TODO: sophistication
    if temperature < 1.0:
        return 0
    return random.random()


# Our URL configuration


urlpatterns = [
    path("", index),
    path("api/predict-rain/", predict_rain),
]

# Create a WSGI application so a web server could run this for us:
app = get_wsgi_application()

# Allow running Django's commands through this file:
if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
