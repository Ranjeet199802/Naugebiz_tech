# Python code to register models in Django admin panel

from django.contrib import admin
from .models import User, Attendance_log, Course, Students, Departments

# Registering models in Django admin panel
admin.site.register(User)
admin.site.register(Attendance_log)
admin.site.register(Course)
admin.site.register(Students)
admin.site.register(Departments)
