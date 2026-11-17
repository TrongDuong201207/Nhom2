from django.contrib import admin
from .models import Course, CourseSection

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'is_active')
    search_fields = ('course_code', 'course_name')
    list_filter = ('is_active',)

@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'section_code', 'semester', 'academic_year', 'teacher_user', 'status')
    list_filter = ('semester', 'academic_year', 'status')
    search_fields = ('course__course_code', 'section_code')
