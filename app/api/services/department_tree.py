"""Файл для проверки бизнес-логиики приложения на зацикливание."""

from rest_framework.validators import ValidationError


def validate_department_cycle(department, new_parent):
    """
    Проверка циклической зависимости
    при изменении parent.
    """

    if not new_parent:
        return

    current = new_parent

    while current is not None:
        if current.id == department.id:
            raise ValidationError("Нельзя создать цикл в дереве.")
        current = current.parent
