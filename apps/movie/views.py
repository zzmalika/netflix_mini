from django.db import models
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from apps.movie import service
from apps.movie import serializers, paginations, models, filters


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильма"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.MovieFilter
    pagination_class = paginations.PaginationNetflix

    def get_queryset(self):
        movies = models.Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                "ratings",
                filter=models.Q(ratings__ip=service.get_client_ip(self.request))
            )
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MovieListSerializer
        elif self.action == 'retrieve':
            return serializers.MovieDetailSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Отзыв для фильма"""
    serializer_class = serializers.ReviewSerializer


# class AddStarRatingViewSet(viewsets.ModelViewSet):
#     """Добавление рейтинга фильму"""
#     serializer_class = serializers.ReviewCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=service.get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров и режиссеров"""
    queryset = models.Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ActorListSerializer
        elif self.action == 'retrieve':
            return serializers.ActorDetailSerializer
