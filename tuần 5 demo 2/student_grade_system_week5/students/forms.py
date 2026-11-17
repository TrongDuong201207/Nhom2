from django import forms
from .models import Student
from accounts.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_code', 'full_name', 'administrative_class', 'email', 'user']
        labels = {
            'student_code': 'Mã sinh viên',
            'full_name': 'Họ và tên',
            'administrative_class': 'Lớp hành chính',
            'email': 'Email',
            'user': 'Tài khoản đăng nhập (nếu đã cấp)',
        }
        widgets = {'user': forms.Select(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(role=User.Role.STUDENT, is_active=True).order_by('username')
        self.fields['user'].required = False

    def clean_student_code(self):
        value = self.cleaned_data['student_code'].strip().upper()
        qs = Student.objects.filter(student_code=value)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Mã sinh viên đã tồn tại.')
        return value

    def clean_full_name(self):
        value = ' '.join(self.cleaned_data['full_name'].split())
        if not value:
            raise forms.ValidationError('Họ tên không được để trống.')
        return value
