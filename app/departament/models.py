"""
Модели проекта organization_api

-Departaments - Позволяет хранить структуру организации
"""

from django.db import models

from core.constant import MAX_LENGTH_NAME_FEILD


class Department(models.Model):
    """
    Модель для представления департамента организации

    Поддерживает иерархическую структуру, где каждый депортамент
    может иметь один вышестоящий отдел.
    """

    name = models.CharField(
        verbose_name="Название",
        max_length=MAX_LENGTH_NAME_FEILD,
    )
    parent_id = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="departments",
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        """Meta-класс модели Department."""

        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"
        indexes = [models.Index(fields=["parent_id"])]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "parent_id"],
                name="unique_departament_name_per_parent",
            )
        ]

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Модель для информации о сотруднике."""

    full_name = models.CharField(
        verbose_name="Полное имя",
        max_length=MAX_LENGTH_NAME_FEILD,
    )
    position = models.CharField(
        verbose_name="Позиция",
        max_length=MAX_LENGTH_NAME_FEILD,
    )
    hired_at = models.DateField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    department_id = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    class Meta:
        """Класс Meta модели Employee."""

        ordering = ["created_at"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.full_name
