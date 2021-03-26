import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_GET

settings.configure(
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    # Disable host header validation:
    ALLOWED_HOSTS=["*"],
    # This module is the urlconf:
    ROOT_URLCONF=__name__,
    # We aren't using any security features but Django requires this setting:
    SECRET_KEY=get_random_string(50),
    # Add some useful defaults:
    MIDDLEWARE=["django.middleware.common.CommonMiddleware"],
)


@require_GET
def index(request):
    return HttpResponse("<h1>Hello World from Django!</h1>")


urlpatterns = [
    path("", index),
]

app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
