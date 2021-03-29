import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_GET
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

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


@require_GET
def index_view(request):
    return HttpResponse(
        "<h1>Welcome to Example Corp</h1>"
        + '<p>See <a href="/api/">/api/</a> for the API.</p>'
    )


@api_view()
def api_index_view(request):
    return Response(
        data={
            "endpoints": [
                "/api/predict-iris/",
            ],
        },
    )


iris = load_iris()
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(iris.data, iris.target)


class IrisInputSerializer(serializers.Serializer):
    sepal_length = serializers.FloatField(min_value=0.0, max_value=10.0)
    sepal_width = serializers.FloatField(min_value=0.0, max_value=10.0)
    petal_length = serializers.FloatField(min_value=0.0, max_value=10.0)
    petal_width = serializers.FloatField(min_value=0.0, max_value=10.0)


@api_view()
def predict_iris_view(request):
    serializer = IrisInputSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    sepal_length = serializer.validated_data["sepal_length"]
    sepal_width = serializer.validated_data["sepal_width"]
    petal_length = serializer.validated_data["petal_length"]
    petal_width = serializer.validated_data["petal_width"]

    prediction = classifier.predict(
        [[sepal_length, sepal_width, petal_length, petal_width]]
    )

    return Response(data={"prediction": prediction})


# Our URL configuration


urlpatterns = [
    path("", index_view),
    path("api/", api_index_view),
    path("api/predict-iris/", predict_iris_view),
]

# Create a WSGI application so a web server could run this for us:
app = get_wsgi_application()

# Allow running Django's commands through this file:
if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
