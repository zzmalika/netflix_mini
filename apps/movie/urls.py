from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.movie import views

router = DefaultRouter()
router.register('movie', views.MovieViewSet)
router.register('review', views.ReviewCreateViewSet)
router.register('rating', views.AddStarRatingViewSet)
router.register('actor', views.ActorsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
