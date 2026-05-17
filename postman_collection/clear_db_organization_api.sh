#!/bin/bash

# Script to clean database from test objects

cd "$(dirname "$0")/../app" || exit

python manage.py shell << EOF
from departament.models import Department, Employee

# Delete all departments (this will automatically delete all employees due to on_delete=CASCADE)
Department.objects.all().delete()

print("Database cleaned successfully")
print("All departments deleted")
print("All employees deleted")
EOF
