""" "Файл сериализаторов приложения Organization_api."""

from rest_framework import serializers

from core.constant import DEFAULT_NUMBER_DEPTH, MINIMUM_ALLOWED_DEPTH, RECURSION_NUMBER_DEPTH
from departament.models import Department, Employee


class DepartamenCreatetSerializer(serializers.ModelSerializer):
    """Серилизатор для создания объекта."""

    class Meta:
        """Класс meta для DepartamenCreatetSerializer"""

        model = Department
        fields = ("id", "name", "parent_id", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_name(self, value):
        """Провека поля на пустоту и удаление проеблов."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Поле не может быть пустым.")
        return value


class EmployeeSerialiser(serializers.ModelSerializer):
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


class Employ

class DepartmentDetailSerializer(serializers.ModelSerializer):
    """Получение детальной информации о подразделении."""

    employees = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        """Класс meta для DepartmentDetailSerializer."""

        model = Department
        fields = (
            "id",
            "name",
            "created_at",
            "employees",
            "children",
        )

    def get_employees(self, obj):
        """Возвращает списк сотрудников подразделения."""
        include_employees = self.context.get("include_employees", True)

        if not include_employees:
            return []

        employees = obj.employees.all()
        return EmployeeSerialiser(
            employees,
            many=True,
        ).data

    def get_children(self, obj):
        """Возвращает список подразделений."""
        depth = self.context.get("depth ", DEFAULT_NUMBER_DEPTH)

        if depth <= MINIMUM_ALLOWED_DEPTH:
            return []

        children = obj.departments.all()
        return DepartmentDetailSerializer(
            children,
            many=True,
            context = {
                **self.context,
                "depth": RECURSION_NUMBER_DEPTH,
            }
        )