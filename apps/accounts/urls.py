from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts.views import ProfileViewSet

router = DefaultRouter()
router.register('profile/', ProfileViewSet, basename='User')

urlpatterns = [
    path('', include(router.urls)),
]
