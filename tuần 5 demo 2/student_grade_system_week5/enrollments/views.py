from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from accounts.permissions import manager_required
from .forms import EnrollmentForm
from .models import Enrollment
from .services import assign_student

@manager_required
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student', 'course_section', 'course_section__course')
    return render(request, 'enrollments/list.html', {'enrollments': enrollments})

@manager_required
def enrollment_create(request):
    form = EnrollmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            assign_student(student=form.cleaned_data['student'], course_section=form.cleaned_data['course_section'])
            messages.success(request, 'Đã gán sinh viên vào lớp học phần.')
            return redirect('enrollments:list')
        except ValidationError as exc:
            form.add_error(None, exc.message)
        except IntegrityError:
            form.add_error(None, 'Đăng ký bị trùng; vui lòng tải lại danh sách.')
    return render(request, 'enrollments/form.html', {'form': form})
