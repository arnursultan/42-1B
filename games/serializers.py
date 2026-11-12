from rest_framework import serializers

from .models import Game, Developer, Platform

class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer

        fields = [
            "id",
            "name",
            "country",
            "founded_year",
        ]

class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform

        fields = [
            "id",
            "name",
            "manufacturer",
        ]

class GameSerializer(serializers.ModelSerializer):

    developer = DeveloperSerializer(read_only=True)

    platforms = PlatformSerializer(
        many=True,
        read_only=True
    )

    developer_id = serializers.PrimaryKeyRelatedField(
        source="developer",
        queryset=Developer.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    platform_ids = serializers.PrimaryKeyRelatedField(
        source="platforms",
        queryset=Platform.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Game

        fields = [
            "id",
            "title",
            "genre",
            "rating",
            "released",
            "developer",
            "developer_id",
            "platforms",
            "platform_ids",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]