import pytest
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(_quantity=1, **kwargs):
        def create_one(index=None):
            defaults = {
                "name": kwargs.get("name", f"Student{index}" if index is not None else "Student"),
                "birth_date": kwargs.get("birth_date", None),
            }
            return Student.objects.create(**defaults)

        if _quantity > 1:
            return [create_one(i) for i in range(_quantity)]
        return create_one()

    return factory


@pytest.fixture
def course_factory():
    def factory(_quantity=1, **kwargs):
        students = kwargs.pop("students", [])

        def create_one(index=None):
            defaults = {
                "name": kwargs.get("name", f"Course{index}" if index is not None else "Course"),
            }
            course = Course.objects.create(**defaults)
            if students:
                course.students.set(students)
            return course

        if _quantity > 1:
            return [create_one(i) for i in range(_quantity)]
        return create_one()

    return factory