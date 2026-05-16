"""Файл для базовых сериализаторов."""

from rest_framework import serializers

from departament.models import Department


class BaseDepartamentSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для departmet."""

    class Meta:
        """Класс meta для BaseDepartamentSerializer"""

        model = Department
        fields = ("id", "name", "parent", "created_at")
        read_only_fields = ("id", "created_at")
