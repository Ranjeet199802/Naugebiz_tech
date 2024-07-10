# This is a Python code file for a Django REST framework application that defines two API views for handling Department objects. The DepartmentListCreate view allows for listing and creating Department objects, while the DepartmentRetrieveUpdateDestroy view allows for retrieving, updating, and deleting Department objects. Both views require authentication for access and support filtering by department_name.

from rest_framework import generics, permissions, filters
from .models import Departments
from .serializers import DepartmentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["department_name"]


class DepartmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
