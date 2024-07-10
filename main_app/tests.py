# For writing unit test cases for the Django Rest Framework code provided, we can use the Django test framework which provides powerful tools for testing Django applications.

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .models import Course, Departments, Students
from .attendance_log import AttendanceLogListCreate
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AttendanceLogListCreateTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.factory = APIRequestFactory()
        self.attendance_log_data = {
            "date": "2022-01-01",
            "status": "Present",
            "employee_id": 1,
        }

    def test_list_attendance_logs_positive(self):
        request = self.factory.get("/attendance_logs/")
        request.user = self.user
        response = AttendanceLogListCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_attendance_logs_negative_unauthenticated(self):
        request = self.factory.get("/attendance_logs/")
        response = AttendanceLogListCreate.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_attendance_log_positive(self):
        request = self.factory.post("/attendance_logs/", self.attendance_log_data)
        request.user = self.user
        response = AttendanceLogListCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_create_attendance_log_negative_invalid_data(self):
        invalid_data = {"date": "2022-01-01", "status": "Invalid", "employee_id": 1}
        request = self.factory.post("/attendance_logs/", invalid_data)
        request.user = self.user
        response = AttendanceLogListCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_create_attendance_log_negative_unauthenticated(self):
        request = self.factory.post("/attendance_logs/", self.attendance_log_data)
        response = AttendanceLogListCreate.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_attendance_log_negative_missing_data(self):
        missing_data = {"date": "2022-01-01", "employee_id": 1}
        request = self.factory.post("/attendance_logs/", missing_data)
        request.user = self.user
        response = AttendanceLogListCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)


class CourseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_course_list_create_positive(self):
        response = self.client.post("/courses/", {"class": "Math"})
        self.assertEqual(
            response.status_code, 201
        )  # Check if course creation is successful

        response = self.client.get("/courses/")
        self.assertEqual(
            response.status_code, 200
        )  # Check if course listing is successful

    def test_course_list_create_negative(self):
        response = self.client.post("/courses/", {})  # Missing required field
        self.assertEqual(
            response.status_code, 400
        )  # Check if bad request status is returned

    def test_course_retrieve_update_destroy_positive(self):
        course = Course.objects.create(cclass="Science")
        response = self.client.get(f"/courses/{course.id}/")
        self.assertEqual(
            response.status_code, 200
        )  # Check if course retrieval is successful

        response = self.client.put(f"/courses/{course.id}/", {"class": "Physics"})
        self.assertEqual(
            response.status_code, 200
        )  # Check if course update is successful

        response = self.client.delete(f"/courses/{course.id}/")
        self.assertEqual(
            response.status_code, 204
        )  # Check if course deletion is successful

    def test_course_retrieve_update_destroy_negative(self):
        response = self.client.get("/courses/999/")  # Non-existent course ID
        self.assertEqual(
            response.status_code, 404
        )  # Check if not found status is returned

        course = Course.objects.create(cclass="History")
        response = self.client.put(
            f"/courses/{course.id}/", {}
        )  # Missing required field
        self.assertEqual(
            response.status_code, 400
        )  # Check if bad request status is returned


class DepartmentAPITestCase(APITestCase):
    def setUp(self):
        self.department_data = {"department_name": "Test Department"}
        self.department = Departments.objects.create(department_name="Test Department")

    # Positive test case for DepartmentListCreate view
    def test_department_list_create_view(self):
        url = reverse("department-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, self.department_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Negative test case for DepartmentListCreate view
    def test_department_list_create_view_invalid_data(self):
        url = reverse("department-list-create")
        invalid_data = {"invalid_field": "Invalid Value"}
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Positive test case for DepartmentRetrieveUpdateDestroy view
    def test_department_retrieve_update_destroy_view(self):
        url = reverse(
            "department-retrieve-update-destroy", kwargs={"pk": self.department.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_data = {"department_name": "Updated Department Name"}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Negative test case for DepartmentRetrieveUpdateDestroy view
    def test_department_retrieve_update_destroy_view_invalid_id(self):
        url = reverse("department-retrieve-update-destroy", kwargs={"pk": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        invalid_data = {"invalid_field": "Invalid Value"}
        response = self.client.put(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StudentsListCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_students_positive(self):
        response = self.client.get("/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_positive(self):
        data = {"name": "John Doe", "age": 20, "class": "Senior", "user": 1}
        response = self.client.post("/students/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_students_negative(self):
        response = self.client.get("/students/")
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_negative(self):
        data = {"name": "Jane Doe", "age": 25, "class": "Junior", "user": 2}
        response = self.client.post("/students/", data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StudentsRetrieveUpdateDestroyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_student_positive(self):
        student = Students.objects.create(
            name="Alice", age=22, sclass="Junior", user_id=3
        )
        response = self.client.get(f"/students/{student.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_positive(self):
        student = Students.objects.create(
            name="Bob", age=21, sclass="Senior", user_id=4
        )
        data = {"name": "Bobby", "age": 22, "class": "Senior", "user": 4}
        response = self.client.put(f"/students/{student.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_student_positive(self):
        student = Students.objects.create(
            name="Charlie", age=23, sclass="Senior", user_id=5
        )
        response = self.client.delete(f"/students/{student.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_student_negative(self):
        response = self.client.get("/students/999/")  # Assuming ID 999 does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_student_negative(self):
        data = {
            "name": "Invalid",
            "age": 30,
            "class": "Invalid",
            "user": 999,  # Assuming user ID 999 does not exist
        }
        response = self.client.put("/students/999/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_student_negative(self):
        response = self.client.delete(
            "/students/999/"
        )  # Assuming ID 999 does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SignupViewTestCase(APITestCase):
    def test_signup_view_positive(self):
        data = {
            "username": "test_user",
            "password": "test_password",
        }
        response = self.client.post("/signup/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("refresh" in response.data)
        self.assertTrue("access" in response.data)

    def test_signup_view_negative(self):
        data = {
            "username": "test_user",
        }
        response = self.client.post("/signup/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )

    def test_login_view_positive(self):
        data = {
            "username": "test_user",
            "password": "test_password",
        }
        response = self.client.post("/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in response.data)
        self.assertTrue("access" in response.data)

    def test_login_view_negative(self):
        data = {
            "username": "test_user",
            "password": "wrong_password",
        }
        response = self.client.post("/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
