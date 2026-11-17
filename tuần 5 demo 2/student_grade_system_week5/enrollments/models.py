from django.db import models
from students.models import Student
from academics.models import CourseSection

class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = 'ENROLLED', 'Đang học'
        CANCELLED = 'CANCELLED', 'Đã hủy'
        COMPLETED = 'COMPLETED', 'Hoàn thành'

    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='enrollments')
    course_section = models.ForeignKey(CourseSection, on_delete=models.PROTECT, related_name='enrollments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ENROLLED)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course_section', 'student']
        constraints = [models.UniqueConstraint(
            fields=['student', 'course_section'], name='uq_student_course_section'
        )]
        verbose_name = 'Lượt đăng ký'
        verbose_name_plural = 'Lượt đăng ký'

    def __str__(self):
        return f'{self.student.student_code} - {self.course_section}'
