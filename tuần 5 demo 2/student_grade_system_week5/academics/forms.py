from django import forms
from .models import Course, CourseSection

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credits', 'description', 'is_active']
        labels = {
            'course_code': 'Mã học phần', 'course_name': 'Tên học phần',
            'credits': 'Số tín chỉ', 'description': 'Mô tả', 'is_active': 'Đang sử dụng',
        }

    def clean_course_code(self):
        value = self.cleaned_data['course_code'].strip().upper()
        qs = Course.objects.filter(course_code=value)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Mã học phần đã tồn tại.')
        return value

class CourseSectionForm(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ['course', 'section_code', 'semester', 'academic_year', 'teacher_user', 'status']
        labels = {
            'course': 'Học phần', 'section_code': 'Mã lớp học phần', 'semester': 'Học kỳ',
            'academic_year': 'Năm học', 'teacher_user': 'Giảng viên phụ trách', 'status': 'Trạng thái',
        }
        widgets = {'course': forms.Select(), 'teacher_user': forms.Select(), 'status': forms.Select()}

    def clean(self):
        cleaned = super().clean()
        course = cleaned.get('course')
        if course and not course.is_active:
            self.add_error('course', 'Không thể mở lớp từ học phần đã vô hiệu hóa.')
        return cleaned
