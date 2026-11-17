from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from academics.models import CourseSection
from .models import Enrollment

@transaction.atomic
def assign_student(*, student, course_section):
    """Tạo lượt đăng ký an toàn; UNIQUE ở DB là lớp bảo vệ cuối cùng chống race condition."""
    if not student:
        raise ValidationError('Phải chọn sinh viên.')
    if not course_section or course_section.status != CourseSection.Status.OPEN:
        raise ValidationError('Lớp học phần không tồn tại hoặc không nhận đăng ký mới.')
    if not course_section.course.is_active:
        raise ValidationError('Học phần đã bị vô hiệu hóa.')
    if Enrollment.objects.filter(student=student, course_section=course_section).exists():
        raise ValidationError('Sinh viên đã được gán vào lớp học phần này.')
    try:
        return Enrollment.objects.create(student=student, course_section=course_section)
    except IntegrityError as exc:
        raise ValidationError('Đăng ký bị trùng; dữ liệu chưa được ghi.') from exc
