# This is a Python code file for managing students using Django Rest Framework.
# It defines two API views - StudentsListCreate for listing and creating students, and StudentsRetrieveUpdateDestroy for retrieving, updating, and deleting students.

from rest_framework import generics, permissions, filters
from .models import Students
from .serializers import StudentsSerializer
from django_filters.rest_framework import DjangoFilterBackend


class StudentsListCreate(generics.ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["class", "user__full_name"]


class StudentsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = [permissions.IsAuthenticated]
