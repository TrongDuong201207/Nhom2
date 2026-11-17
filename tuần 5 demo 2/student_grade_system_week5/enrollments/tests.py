from django.test import TestCase
from django.db import IntegrityError, transaction
from students.models import Student
from academics.models import Course, CourseSection
from .models import Enrollment
from .services import assign_student
from django.core.exceptions import ValidationError

class EnrollmentTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(student_code='25070011', full_name='Nguyễn Minh Anh', administrative_class='CNTT-K68', email='a@example.local')
        course = Course.objects.create(course_code='CS101', course_name='Nhập môn lập trình', credits=3)
        self.section = CourseSection.objects.create(course=course, section_code='CS101-01', semester='1', academic_year='2026-2027', status=CourseSection.Status.OPEN)

    def test_assign_student_success(self):
        enrollment = assign_student(student=self.student, course_section=self.section)
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_duplicate_enrollment_is_rejected(self):
        assign_student(student=self.student, course_section=self.section)
        with self.assertRaises(ValidationError):
            assign_student(student=self.student, course_section=self.section)

    def test_closed_section_rejects_enrollment(self):
        self.section.status = CourseSection.Status.CLOSED
        self.section.save()
        with self.assertRaises(ValidationError):
            assign_student(student=self.student, course_section=self.section)
