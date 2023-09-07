# import os
# from django.core.asgi import get_asgi_application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

# application = get_asgi_application()
# from channels.routing import ProtocolTypeRouter,URLRouter
# from django.urls import path
# from premium.consumers import ChatConsumer

# ws_pattern = [
#     path('chat/<room_code>', ChatConsumer.as_asgi())
# ]


# application = ProtocolTypeRouter(

#     {
#         'websocket' : (URLRouter(ws_pattern))
#     }
# )

# import os
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from premium.consumers import ChatConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'premium.settings')

# django_asgi_app = get_asgi_application()


# ws_pattern = [
#     path('chat/<str:room_code>', ChatConsumer.as_asgi())
# ]

# application = ProtocolTypeRouter(
#     {
#         'http': django_asgi_app,
#         'websocket': URLRouter(ws_pattern),     
#     }
# )
