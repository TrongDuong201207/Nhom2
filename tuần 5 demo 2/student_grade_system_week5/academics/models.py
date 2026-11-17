from django.conf import settings
from django.db import models

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=150)
    credits = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course_code']
        verbose_name = 'Học phần'
        verbose_name_plural = 'Học phần'

    def __str__(self):
        return f'{self.course_code} - {self.course_name}'

class CourseSection(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Nháp'
        OPEN = 'OPEN', 'Đang mở'
        IN_PROGRESS = 'IN_PROGRESS', 'Đang học'
        CLOSED = 'CLOSED', 'Đã đóng'
        COMPLETED = 'COMPLETED', 'Hoàn tất'

    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='sections')
    section_code = models.CharField(max_length=30)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)
    teacher_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='teaching_sections'
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['academic_year', 'semester', 'section_code']
        constraints = [models.UniqueConstraint(
            fields=['course', 'section_code', 'semester', 'academic_year'],
            name='uq_course_section_term_year'
        )]
        verbose_name = 'Lớp học phần'
        verbose_name_plural = 'Lớp học phần'

    def __str__(self):
        return f'{self.course.course_code} - {self.section_code} ({self.semester}/{self.academic_year})'
