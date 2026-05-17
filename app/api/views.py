"""View-s для organization_api."""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services.department_delete import delete_with_cascade, delete_with_reassign
from api.serializers.departament import (
    DepartmentCreateSerializer,
    DepartmentUpdateSerializer,
    DepartmentDetailSerializer,
    EmployeeSerializer,
)
from api.validations import DepartmentDeleteValidator

from core.constant import DEFAULT_NUMBER_DEPTH, MIN_DEPTH, MAX_DEPTH
from departament.models import Department


# Create your views here.
class DepartmentAPIView(APIView):
    """APIView для работы с подразделениями."""

    def get(self, request, pk):
        """Метод GET для получения объекта."""
        try:
            depth = int(request.query_params.get("depth", DEFAULT_NUMBER_DEPTH))
        except ValueError:
            depth = DEFAULT_NUMBER_DEPTH

        depth = max(MIN_DEPTH, min(depth, MAX_DEPTH))

        include_employees = (
            request.query_params.get(
                "include_employees",
                "true",
            ).lower()
            == "true"
        )
        department_queryset = Department.objects.prefetch_related(
            "employees",
            "children",
        )
        department = get_object_or_404(
            department_queryset,
            id=pk,
        )
        serializer = DepartmentDetailSerializer(
            department,
            context={
                "depth": depth,
                "include_employees": include_employees,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        """Метод POST для создания объекта."""
        serializer = DepartmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        """Метод PUTCH для обновления объекта."""
        department = get_object_or_404(Department, id=pk)
        serializer = DepartmentUpdateSerializer(
            instance=department,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """Удаление департамента."""
        validator = DepartmentDeleteValidator(request, pk)
        validated_data = validator.validate()

        mode = validated_data["mode"]
        department = get_object_or_404(Department, id=pk)

        if mode == "reassign":
            reassign_id = validated_data["reassign_id"]
            reassign_department = get_object_or_404(Department, id=reassign_id)
            delete_with_reassign(department, reassign_department)

        elif mode == "cascade":
            delete_with_cascade(department)

        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeAPIView(APIView):
    """APIview для работы с пользователями."""

    def post(self, request, pk):
        """Создание пользователя в подразделении."""
        department = get_object_or_404(Department, id=pk)
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(department=department)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
