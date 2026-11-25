
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

from .models import CityCover, CityPost, Location, SearchHistory


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'


class CityCoverSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = CityCover
        fields = ['id', 'city', 'image', 'uploaded_by', 'updated_at']
        read_only_fields = ['id', 'uploaded_by', 'updated_at']

    def validate_city(self, value):
        city = value.strip()
        if not city:
            raise serializers.ValidationError('Вкажіть місто.')
        matches = CityCover.objects.filter(city__iexact=city)
        if self.instance:
            matches = matches.exclude(pk=self.instance.pk)
        if matches.exists():
            raise serializers.ValidationError('Для цього міста вже є головне фото.')
        return city

    def validate_image(self, value):
        if value.size > 8 * 1024 * 1024:
            raise serializers.ValidationError('Фото має бути не більше 8 МБ.')
        return value


class CityPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = CityPost
        fields = ['id', 'city', 'title', 'body', 'image', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_image(self, value):
        if value.size > 8 * 1024 * 1024:
            raise serializers.ValidationError('Фото має бути не більше 8 МБ.')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
