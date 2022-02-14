from django.urls import path
from .views import create_driver, logout, google, refresh, signup, send_otp, get_cred, create_dealer, create_driver, get_driver, get_dealer, get_drivers_list

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/token/', TokenRefreshView.as_view(), name="refresh"),
    path('verify/', TokenVerifyView.as_view(), name="verify"),
    path('logout/', logout, name="logout"),
    path('refresh/', refresh),
    
    path('google/', google),
    
    path('signup/', signup),
    
    path('send_otp/', send_otp),
    
    path('otp_login/', get_cred),
    
    path('create_driver/', create_driver),
    path('get_driver/', get_driver),
    
    path('create_dealer/', create_dealer),
    path('get_dealer/', get_dealer),
    
    path('get_drivers_list/', get_drivers_list),
]