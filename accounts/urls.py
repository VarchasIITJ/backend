from .views import UserViewSet, GroupViewSet
from django.urls import path, include
from rest_framework import routers
from .views import google_signup,LoginUserView,RegisterUserView,userleaveTeam,userjoinTeam,userDisplayteam,userDisplayProfile,PasswordReset,OTPVerification,restpassword,resendpassword,UpdateUserInfoView
app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('userregister/',RegisterUserView.as_view(),name='userregister'),   
    
    path('google-signup/',google_signup),


    path('updateInfo/', UpdateUserInfoView.as_view(), name='update-info'),
    
    path('userlogin/',LoginUserView,name='userlogin'),
    
    path('jointeam/', userjoinTeam, name='userjoinTeam'),
    path('leaveteam/', userleaveTeam, name='userleaveTeam'),
    path('displayTeam/',userDisplayteam,name='userDisplayteam'),
    path('displayProfile/',userDisplayProfile,name='userDisplayprofile'),
    path('password_reset_request/',PasswordReset.as_view(),name='passwordrequest'),
    path('otp_verification/',OTPVerification.as_view(),name='otpverification'),
    path('reset_password/',restpassword,name='restpassword'),
    path('resendpassword/',resendpassword,name='resendpassword'),
]
