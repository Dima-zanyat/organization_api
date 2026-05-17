"""Файл валидации данных."""

from rest_framework.exceptions import ValidationError

from core.constant import MODE_DELETES


class DepartmentDeleteValidator:
    """Класс для валидации данных при удалении."""

    def __init__(self, request, pk):
        self.request = request
        self.pk = pk
        self.query_params = request.query_params

    def get_and_validate_data(self) -> dict:
        """Цепочка проверок с возвратом словаря проверенных данных."""
        mode = self._validate_mode(self.query_params.get("mode"))

        # Задаем дефолтные значения, чтобы избежать KeyError во View
        validate_data = {"mode": mode, "reassign_id": None}

        if mode == "reassign":
            reassign_id_raw = self.query_params.get("reassign_to_department_id")
            validate_data["reassign_id"] = self._validate_reassign(reassign_id_raw)

        return validate_data

    def _validate_mode(self, mode):
        """Валидация параметра режима удаления."""
        if not mode:
            raise ValidationError("В параметрах запроса отсутствует mode.")
        if mode not in MODE_DELETES:
            raise ValidationError("Выберите режим удаления из ('cascade', 'reassign').")
        return mode

    def _validate_reassign(self, reassign_id_raw):
        """Валидация ID департамента для переназначения."""
        if not reassign_id_raw:
            raise ValidationError("Параметр 'reassign_to_department_id' обязателен.")
        try:
            reassign_id = int(reassign_id_raw)
        except ValueError:
            raise ValidationError("reassign_to_department_id должен быть числом.")

        if reassign_id == int(self.pk):
            raise ValidationError(
                "Нельзя переназначить сотрудников в удаляемый департамент."
            )

        return reassign_id
