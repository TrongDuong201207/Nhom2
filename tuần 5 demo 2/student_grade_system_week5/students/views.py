from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from accounts.permissions import manager_required
from .forms import StudentForm
from .models import Student

@manager_required
def student_list(request):
    q = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if q:
        students = students.filter(student_code__icontains=q) | students.filter(full_name__icontains=q)
    return render(request, 'students/list.html', {'students': students, 'q': q})

@manager_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})

@manager_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã tạo hồ sơ sinh viên.')
        return redirect('students:list')
    return render(request, 'students/form.html', {'form': form, 'title': 'Thêm sinh viên'})

@manager_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã cập nhật hồ sơ sinh viên.')
        return redirect('students:detail', pk=student.pk)
    return render(request, 'students/form.html', {'form': form, 'title': 'Sửa hồ sơ sinh viên'})

@manager_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        try:
            student.delete()
            messages.success(request, 'Đã xóa hồ sơ sinh viên chưa phát sinh đăng ký.')
        except ProtectedError:
            messages.error(request, 'Không thể xóa sinh viên đã có đăng ký học phần; hãy giữ hồ sơ để bảo toàn lịch sử.')
        return redirect('students:list')
    return render(request, 'students/confirm_delete.html', {'student': student})
