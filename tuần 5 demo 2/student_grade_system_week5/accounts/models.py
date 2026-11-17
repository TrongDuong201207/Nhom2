from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

class UserManager(DjangoUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Sinh viên'
        LECTURER = 'LECTURER', 'Giảng viên'
        ACADEMIC_STAFF = 'ACADEMIC_STAFF', 'Giáo vụ'
        ADMIN = 'ADMIN', 'Quản trị'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    objects = UserManager()

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
