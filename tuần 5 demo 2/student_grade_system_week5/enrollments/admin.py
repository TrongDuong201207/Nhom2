from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_section', 'status', 'registered_at')
    list_filter = ('status', 'course_section__semester', 'course_section__academic_year')
    search_fields = ('student__student_code', 'student__full_name', 'course_section__section_code')
