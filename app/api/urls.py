"""Файл URL для api приложения organization_api."""

from django.urls import include, path

from .views import DepartmentAPIView, EmployeeAPIView

urlpatterns = [
    path(
        "departments/",
        DepartmentAPIView.as_view(),
        name="department-create",
    ),
    path(
        "departments/<int:pk>/",
        DepartmentAPIView.as_view(),
        name="department-detail",
    ),
    path(
        "departments/<int:pk>/employees/",
        EmployeeAPIView.as_view(),
        name="employee-create",
    ),
]
