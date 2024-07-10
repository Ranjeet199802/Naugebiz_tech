# Python code for defining models for a Django application. Includes classes for users, departments, courses, students, and attendance logs.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    submitted_by = models.CharField(max_length=200)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    USER_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("student", "Student"),
    )
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    submitted_by = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Departments(BaseModel):
    department_name = models.CharField(max_length=200)

    def __str__(self):
        return self.department_name


class Course(BaseModel):
    course_name = models.CharField(max_length=200)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    semester = models.CharField(max_length=200)
    cclass = models.CharField(max_length=200)
    lecture_hours = models.CharField(max_length=200)

    def __str__(self):
        return self.course_name


class Students(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    sclass = models.CharField(max_length=200)


class Attendance_log(BaseModel):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    Course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return self.student.full_name
