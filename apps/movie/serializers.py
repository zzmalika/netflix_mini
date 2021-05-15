from rest_framework import serializers

from apps.movie import models


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """Вывод списка категории"""

    class Meta:
        model = models.Category
        exclude = [
            'created_at', 'updated_at', 'deleted_at', 'is_deleted'
        ]


class GenreSerializer(serializers.ModelSerializer):
    """Вывод списка жанров"""

    class Meta:
        model = models.Genre
        exclude = [
            'created_at', 'updated_at', 'deleted_at', 'is_deleted'
        ]


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка актеров и режиссеров"""

    class Meta:
        model = models.Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вывод полного описания актеров и режиссеров"""

    class Meta:
        model = models.Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    """Список Фильмов"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = models.Movie
        fields = (
            "id", 'title', 'tagline', 'category', 'rating_user', 'middle_star'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Отзыв"""

    class Meta:
        model = models.Review
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    """Список отзывов"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = models.Review
        fields = ("name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = models.Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""

    class Meta:
        model = models.Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = models.Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
