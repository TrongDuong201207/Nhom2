from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_code', 'full_name', 'administrative_class', 'email')
    search_fields = ('student_code', 'full_name', 'email')
    list_filter = ('administrative_class',)
