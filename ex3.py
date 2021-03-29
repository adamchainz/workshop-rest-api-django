import os
import random
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.utils.crypto import get_random_string

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
    # Django REST Framework settings:
    REST_FRAMEWORK={
        # Disable default authentication
        "DEFAULT_AUTHENTICATION_CLASSES": [],
        "UNAUTHENTICATED_USER": None,
        # Disable default browsable API, since we haven't set TEMPLATES
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
        ],
    },
)

# Django REST Framework requires Django settings to be configured before
# importing it

from rest_framework import serializers  # noqa: E402
from rest_framework.decorators import api_view  # noqa: E402
from rest_framework.response import Response  # noqa: E402

# Our view functions


@api_view()
def index(request):
    return Response(
        data={
            "endpoints": [
                "/api/predict-rain/",
            ],
        },
    )


class PredictRainInputSerializer(serializers.Serializer):
    temperature = serializers.FloatField(
        label="Temperature (Celsius)",
        min_value=-40.0,
        max_value=120.0,
    )


@api_view()
def predict_rain(request):
    serializer = PredictRainInputSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    temperature = serializer.validated_data["temperature"]

    rain_probability = sophisticated_model_to_predict_rain(temperature)

    return Response(data={"rain_probability": rain_probability})


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
