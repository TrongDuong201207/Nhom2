from django.test import TestCase, Client
from django.db import IntegrityError, transaction
from accounts.models import User
from .models import Student

class StudentModelTests(TestCase):
    def test_student_code_must_be_unique(self):
        Student.objects.create(student_code='25070011', full_name='A', administrative_class='CNTT-K68', email='a@example.local')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Student.objects.create(student_code='25070011', full_name='B', administrative_class='CNTT-K68', email='b@example.local')

class StudentViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username='staff', password='DemoPass123!', role=User.Role.ACADEMIC_STAFF)
        self.client = Client()

    def test_staff_can_open_student_list(self):
        self.client.login(username='staff', password='DemoPass123!')
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)

    def test_student_role_cannot_open_staff_student_list(self):
        student_user = User.objects.create_user(username='student', password='DemoPass123!', role=User.Role.STUDENT)
        self.client.login(username='student', password='DemoPass123!')
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 403)
