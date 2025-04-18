
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gethosapp.settings")

# application = get_asgi_application()
import django
django.setup()  # <-- Isso garante que os apps estejam prontos

# Agora sim, podemos importar o routing
import gethos_home.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            gethos_home.routing.websocket_urlpatterns
        )
    ),
})

