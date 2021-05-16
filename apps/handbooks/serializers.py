from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.handbooks.models import Category, Genre, City, Country


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    description = serializers.CharField(
        style={'base_template': 'textarea.html'}
    )

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        return instance


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )
    description = serializers.CharField(
        style={'base_template': 'textarea.html'}
    )

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        return instance


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class CityWithCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'country_name')

    country_name = serializers.ReadOnlyField(source='country.name')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

    cities = CitySerializer(source='city_set', required=False, many=True)
