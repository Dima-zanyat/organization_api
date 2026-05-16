""" "Файл сериализаторов приложения Organization_api."""

from rest_framework import serializers

from departament.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer для сотрудника."""

    class Meta:
        """Класс meta для EmployeeCreateSerialiser."""

        model = Employee
        fields = (
            "id",
            "full_name",
            "position",
            "hired_at",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
