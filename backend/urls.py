from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register',views.MemberCreateView.as_view(),name='register'),
    path('api/basic-register/create',views.BasicDetailsCreateView.as_view(),name='basic-details'),
    path('api/personal-register',views.PersonalDetailsCreateView.as_view(),name='persona-details'),
    path('api/professional-register',views.ProfessionalDetailsCreateView.as_view(),name='professional-details'),
    path('api/about-register',views.AboutDetailsCreateView.as_view(),name='about-details'),
    path('api/otp-verification',views.OTPVerificationView.as_view(),name='otp-verification'),
    path('api/profile-verification', views.ProfileVerificationView.as_view(), name='profile-verification'),
    path('api/adminlogin',views.AdminLoginView.as_view(),name='adminlogin'),
    path('api/verify-member/<int:member_id>',views.AdminMemberVerification.as_view(),name='verify-member'),
    path('api/adminmember', views.AdminMember.as_view(), name='admin-member'),
    path('api/memberlogin',views.MemberLogin.as_view(),name='memberlogin'),
    path('api/imageupload',views.ImageUpload.as_view(),name='imageupload'),
    path('api/allmemberdetails', views.AllMembersView.as_view(), name='allmemberdetails'),
    path('api/references',views.PreferenceCreateView.as_view(),name='references'),
    path('api/adminpremium',views.MembershipPackageView.as_view(),name='premium'),
    path('api/individual/<int:member_id>/',views.IndividalMemberDetails.as_view(),name='individual')





]
