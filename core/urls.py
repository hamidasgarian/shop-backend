from rest_framework import routers
from .views import *
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'user', user_view, basename='user')
router.register(r'role', role_view, basename='role')
router.register(r'product', product_view, basename='product')
router.register(r'sell', sell_view, basename='sell')
router.register(r'tools', tools, basename='tools')


urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]