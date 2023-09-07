from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from premium.consumers import ChatConsumer
from django.urls import re_path
# application = ProtocolTypeRouter({
#     "websocket": URLRouter([
#         path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi())
#     ]),   
# })

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import re_path
# from premium.consumers import ChatConsumer

# application = ProtocolTypeRouter(
#     {
#         "websocket": URLRouter([re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi())]),
#     }
# )



# testing

websocket_urlpatterns = [
    re_path(r'^ws/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
   
]

