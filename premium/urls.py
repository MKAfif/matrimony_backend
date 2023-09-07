from .views import *
from django.urls import path
from premium import views
from django.urls import re_path



urlpatterns = [
    path('api/premium-packages/', views.PremiumUpgrade.as_view(), name='premium-packages'),
    path('api/billing/<int:premium_id>/',views.Billing.as_view(),name='billing'),
    path('api/updatepremiumprofile',views.UpdatePremiumProfile.as_view(),name = 'updatpremium'),
    path('api/premiummembers',views.PremiumMember.as_view(),name='premiummember'),
    path('api/chattingprofiles/', views.ChattingProfiles.as_view(), name='allmemberdetails'),
    

]

# websocket_urlpatterns = [
#     re_path(r'ws/chat/matrimony_chat/$', views.ChatConsumer.as_asgi()),
#     # Define more WebSocket URL patterns if needed
# ]

# urlpatterns += websocket_urlpatterns