# This Python code defines two API views for creating, listing, updating, and deleting Course objects.
# It uses Django REST framework for building the APIs, along with permissions and filters.

from rest_framework import generics, permissions, filters
from .models import Students, Course
from .serializers import CourseSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["class"]


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
