from django.urls import path
from .views import SignupView, LoginView
from .Deparment_app import DepartmentListCreate, DepartmentRetrieveUpdateDestroy
from .attendance_log import AttendanceLogListCreate
from .students import StudentsListCreate, StudentsRetrieveUpdateDestroy
from .course import CourseListCreate, CourseRetrieveUpdateDestroy

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("departments/", DepartmentListCreate.as_view(), name="department-list-create"),
    path(
        "departments/<int:pk>/",
        DepartmentRetrieveUpdateDestroy.as_view(),
        name="department-retrieve-update-destroy",
    ),
    path(
        "attendance_logs/",
        AttendanceLogListCreate.as_view(),
        name="attendance-log-list-create",
    ),
    path("students/", StudentsListCreate.as_view(), name="student-list-create"),
    path(
        "students/<int:pk>/",
        StudentsRetrieveUpdateDestroy.as_view(),
        name="student-retrieve-update-destroy",
    ),
    path("course/", CourseListCreate.as_view(), name="course-list-create"),
    path(
        "course/<int:pk>/",
        CourseRetrieveUpdateDestroy.as_view(),
        name="course-retrieve-update-destroy",
    ),
]
