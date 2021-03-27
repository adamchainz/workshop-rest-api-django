import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_GET

# Configure Django

settings.configure(
    # Use Django's debug mode when the environment asks for it:
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    # Disable security feature - host header validation:
    ALLOWED_HOSTS=["*"],
    # Tell Django to read URL's from this module:
    ROOT_URLCONF=__name__,
    # We aren't using any security features but Django requires this setting:
    SECRET_KEY=get_random_string(50),
    # Add some useful defaults:
    MIDDLEWARE=["django.middleware.common.CommonMiddleware"],
)


# Our view function


@require_GET
def index(request):
    return HttpResponse("<h1>Hello World from Django!</h1>")


# Our URL configuration


urlpatterns = [
    path("", index),
]

# Create a WSGI application so a web server could run this for us:
app = get_wsgi_application()

# Allow running Django's commands through this file:
if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
