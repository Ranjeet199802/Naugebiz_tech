# Python code for serializers related to User, Departments, Attendance_log, Students, and Course models in a Django REST framework project.

from rest_framework import serializers
from .models import User, Departments, Attendance_log, Students, Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "type", "full_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            full_name=validated_data["full_name"],
            type=validated_data["type"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ["id", "department_name", "submitted_by", "updated_at"]


class AttendanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance_log
        fields = "__all__"


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
