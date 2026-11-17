from django import forms
from .models import Enrollment
from students.models import Student
from academics.models import CourseSection

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course_section']
        labels = {'student': 'Sinh viên', 'course_section': 'Lớp học phần'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.order_by('student_code')
        self.fields['course_section'].queryset = CourseSection.objects.select_related('course').filter(
            status=CourseSection.Status.OPEN, course__is_active=True
        )

    def clean(self):
        cleaned = super().clean()
        student = cleaned.get('student')
        section = cleaned.get('course_section')
        if student and section and Enrollment.objects.filter(student=student, course_section=section).exists():
            raise forms.ValidationError('Sinh viên đã được gán vào lớp học phần này.')
        return cleaned
