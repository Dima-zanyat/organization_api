"""Файл для логики удаления департмента по параметрам."""

from django.db import transaction


@transaction.atomic
def delete_with_reassign(
    department,
    reassign_department,
):
    """
    Удаление департамента
    с переносом сотрудников.
    """

    department.employees.update(department=reassign_department)

    department.delete()


@transaction.atomic
def delete_with_cascade(department):
    """Каскадное удаление."""
    department.delete()
