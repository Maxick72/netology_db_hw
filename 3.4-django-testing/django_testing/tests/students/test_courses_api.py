import pytest

from students.models import Course


BASE_URL = "/api/v1/courses/"

@pytest.mark.django_db
def test_get_course_list(api_client, course_factory):
    course_factory(name="Python")
    course_factory(name="Django")

    response = api_client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.data) == 2
    names = {item["name"] for item in response.data}
    assert names == {"Python", "Django"}

@pytest.mark.django_db
def test_get_course_detail(api_client, course_factory):
    course = course_factory(name="Python")

    response = api_client.get(f"{BASE_URL}{course.id}/")

    assert response.status_code == 200
    assert response.data["id"] == course.id
    assert response.data["name"] == "Python"

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name="Old name")

    payload = {
        "name": "New name",
    }

    response = api_client.patch(f"{BASE_URL}{course.id}/", payload, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "New name"

    course.refresh_from_db()
    assert course.name == "New name"

@pytest.mark.django_db
def test_update_course_students(api_client, course_factory, student_factory):
    student_1 = student_factory(name="Ivan")
    student_2 = student_factory(name="Maria")
    course = course_factory(name="Python")

    payload = {
        "name": "Python updated",
        "students": [student_1.id, student_2.id],
    }

    response = api_client.put(f"{BASE_URL}{course.id}/", payload, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Python updated"
    assert set(response.data["students"]) == {student_1.id, student_2.id}

    course.refresh_from_db()
    assert set(course.students.values_list("id", flat=True)) == {student_1.id, student_2.id}

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory(name="Python")

    response = api_client.delete(f"{BASE_URL}{course.id}/")

    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()


@pytest.mark.django_db
def test_filter_course_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    target_course = courses[1]

    response = api_client.get(BASE_URL, {"id": target_course.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == target_course.id

@pytest.mark.django_db
def test_filter_courses_by_multiple_ids(api_client, course_factory):
    courses = course_factory(_quantity=5)
    target_ids = [courses[1].id, courses[3].id]

    response = api_client.get(BASE_URL, [("id", target_ids[0]), ("id", target_ids[1])])

    assert response.status_code == 200
    assert len(response.data) == 2

    response_ids = {item["id"] for item in response.data}
    assert response_ids == set(target_ids)

@pytest.mark.django_db
def test_filter_course_by_name(api_client, course_factory):
    course_factory(name="Python")
    course_factory(name="Django")

    response = api_client.get(BASE_URL, {"name": "Django"})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Django"

@pytest.mark.django_db
def test_create_course_with_empty_name(api_client):
    payload = {
        "name": "",
    }

    response = api_client.post(BASE_URL, payload, format="json")

    assert response.status_code == 400
    assert "name" in response.data






