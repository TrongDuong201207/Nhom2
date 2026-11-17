from django.conf import settings
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='student_profile'
    )
    student_code = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    administrative_class = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_code']
        verbose_name = 'Sinh viên'
        verbose_name_plural = 'Sinh viên'

    def __str__(self):
        return f'{self.student_code} - {self.full_name}'
