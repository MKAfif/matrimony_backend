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
    path('api/getmessage/<int:recepient_id>/',views.GetMessage.as_view(),name = 'getmessage'),
    path('api/checkmembership',views.CheckMembership.as_view(),name='checkmembership')

]

