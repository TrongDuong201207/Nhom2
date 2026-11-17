from django.test import TestCase
from django.db import IntegrityError, transaction
from accounts.models import User
from .models import Course, CourseSection

class CourseSectionConstraintTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(course_code='CS101', course_name='Nhập môn lập trình', credits=3)

    def test_course_code_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Course.objects.create(course_code='CS101', course_name='Tên khác', credits=3)

    def test_section_code_unique_in_course_term_year(self):
        CourseSection.objects.create(course=self.course, section_code='CS101-01', semester='1', academic_year='2026-2027')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CourseSection.objects.create(course=self.course, section_code='CS101-01', semester='1', academic_year='2026-2027')
