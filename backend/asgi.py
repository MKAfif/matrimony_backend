"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from premium.consumers import ChatConsumer
# from django.urls import path
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')


# django_asgi_app = get_asgi_application()

# ws_pattern = [
#     path('chat/<str:room_name>/', ChatConsumer.as_asgi())
# ]

# application = ProtocolTypeRouter(
#     {
#         'http': application,
#         'websocket': URLRouter(ws_pattern),
#     }
# )

# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from premium.routing import websocket_urlpatterns

# django_asgi_app = get_asgi_application()


# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AuthMiddlewareStack(
#             URLRouter(websocket_urlpatterns)
#         ),
#     }
# )



import os
from django.core.asgi import get_asgi_application
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from premium.routing import websocket_urlpatterns
 
application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() ,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )   
        )
    }
)