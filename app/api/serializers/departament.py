""" "Файл сериализаторов приложения Organization_api."""

from rest_framework import serializers

from core.constant import (
    MINIMUM_ALLOWED_DEPTH,
    RECURSION_NUMBER_DEPTH,
)
from api.serializers.base_serializers import BaseDepartamentSerializer
from api.serializers.employee import EmployeeSerializer


class DepartmentCreateSerializer(BaseDepartamentSerializer):
    """Серилизатор для создания объекта."""

    def validate_name(self, value):
        """Провека поля на пустоту и удаление проеблов."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Поле не может быть пустым.")
        return value


class DepartmentUpdateSerializer(BaseDepartamentSerializer):

    def validate(self, attrs):
        """Проверка на циклическую зависимость."""

        new_parent = attrs.get("parent")
        department = self.instance

        if not new_parent:
            return attrs

        current = new_parent

        while current is not None:
            if current.id == department.id:
                raise serializers.ValidationError("Нельзя создать цикл в дереве.")
            current = current.parent
        return attrs


class DepartmentDetailSerializer(BaseDepartamentSerializer):
    """Получение детальной информации о подразделении."""

    employees = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_employees(self, obj):
        """Возвращает список сотрудников подразделения."""
        include_employees = self.context.get("include_employees")

        if not include_employees:
            return []

        employees = obj.employees.all()
        return EmployeeSerializer(
            employees,
            many=True,
        ).data

    def get_children(self, obj):
        """Возвращает список подразделений(рекурсивно)."""
        depth = self.context.get("depth")

        if depth <= MINIMUM_ALLOWED_DEPTH:
            return []

        children = obj.children.all()
        return DepartmentDetailSerializer(
            children,
            many=True,
            context={
                **self.context,
                "depth": depth - RECURSION_NUMBER_DEPTH,
            },
        ).data
