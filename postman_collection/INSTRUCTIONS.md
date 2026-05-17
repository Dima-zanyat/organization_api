# Organization API - Postman коллекция

## Обзор

Создана полная Postman коллекция для тестирования API проекта **organization_api**.

## Созданные файлы

1. **organization_api.postman_collection.json** - Основной файл коллекции
2. **README_organization_api.md** - Подробные инструкции
3. **clear_db_organization_api.sh** - Скрипт для очистки БД

## Что включает коллекция

### 1. Department // Create
- `create_root_department` - Создание корневого departmenta
- `create_child_department` - Создание departmenta с parent'ом

**Тесты проверяют:**
- Статус-код 201
- Структуру ответа (JSON Schema)
- Сохранение ID в переменные коллекции

### 2. Department // Read
- `get_root_department` - Получение departmenta с параметром по умолчанию
- `get_department_with_depth` - Получение departmenta с указанием глубины и включением employees
- `get_department_without_employees` - Получение departmenta без employees

**Тесты проверяют:**
- Статус-код 200
- Структуру ответа
- Корректность фильтрации (include_employees)
- Наличие вложенных departmentов при depth > 0

### 3. Department // Update
- `update_department_name` - Обновление имени departmenta
- `update_department_parent` - Изменение parent departmenta

**Тесты проверяют:**
- Статус-код 200
- Корректное обновление полей
- Сохранение ID departmenta

### 4. Department // Delete
- `delete_department_with_cascade` - Удаление departmenta с каскадным удалением вложенных
- `delete_department_with_reassign` - Удаление departmenta с переназначением вложенных

**Тесты проверяют:**
- Статус-код 204 (No Content)
- Успешное удаление

### 5. Employee // Create
- `create_employee_in_department` - Создание первого сотрудника
- `create_second_employee` - Создание второго сотрудника

**Тесты проверяют:**
- Статус-код 201
- Структуру ответа (JSON Schema)
- Корректность заполнения полей
- Сохранение ID в переменные

### 6. Employee // Verify in Department
- `get_department_with_employees` - Получение departmenta со всеми сотрудниками

**Тесты проверяют:**
- Статус-код 200
- Наличие добавленных employees в departmente
- Корректность данных employees

## Быстрый старт

### Подготовка
```bash
cd app
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### Использование Postman
1. Открыть Postman
2. File → Import → выбрать `organization_api.postman_collection.json`
3. В левой панели нажать на три точки рядом с коллекцией
4. Выбрать "Run collection"
5. Нажать "Run Organization API"

### Очистка БД после тестирования
```bash
cd postman_collection
bash clear_db_organization_api.sh
```

## Переменные коллекции

| Переменная | Значение | Тип |
|-----------|---------|-----|
| baseUrl | http://127.0.0.1:8000 | string |
| departmentName | Отдел разработки | string |
| childDepartmentName | Backend команда | string |
| updatedDepartmentName | Обновлённый отдел разработки | string |
| employeeFullName | Иван Петров | string |
| employeePosition | Senior Backend Developer | string |
| employeeFullName2 | Мария Сидорова | string |
| employeePosition2 | Junior Frontend Developer | string |

Динамические переменные (заполняются автоматически):
- rootDepartmentId
- childDepartmentId
- cascadeDepartmentId
- employeeId
- employeeId2

## Особенности реализации

✅ **Логика соответствует структуре foodgram коллекции:**
- Использование переменных коллекции для хранения ID
- JSON Schema валидация для проверки структуры ответов
- Тесты на каждом шаге для проверки статус-кодов и данных
- Логический порядок запросов (create → read → update → delete)

✅ **Покрытие всех основных операций API:**
- CRUD операции для departments
- Создание и проверка employees
- Тестирование query параметров (depth, include_employees)
- Тестирование различных режимов удаления (cascade, reassign)

✅ **Безопасность:**
- Коллекция не трогает существующий код проекта
- Тесты чистые и независимые
- Предусмотрена очистка БД после тестирования
