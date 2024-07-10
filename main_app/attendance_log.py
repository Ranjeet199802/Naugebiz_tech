# This Python code defines a class AttendanceLogListCreate that uses Django Rest Framework to handle list and create operations for Attendance_log objects. It specifies the queryset, serializer class, and permission classes to be used.

from rest_framework import generics, permissions
from .models import Attendance_log
from .serializers import AttendanceLogSerializer


class AttendanceLogListCreate(generics.ListCreateAPIView):
    queryset = Attendance_log.objects.all()
    serializer_class = AttendanceLogSerializer
    permission_classes = [permissions.IsAuthenticated]
