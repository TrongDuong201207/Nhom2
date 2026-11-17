from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.permissions import staff_required, manager_required
from .forms import CourseForm, CourseSectionForm
from .models import Course, CourseSection

@staff_required
def course_list(request):
    q = request.GET.get('q', '').strip()
    courses = Course.objects.all()
    if q:
        courses = courses.filter(course_code__icontains=q) | courses.filter(course_name__icontains=q)
    return render(request, 'academics/course_list.html', {'courses': courses, 'q': q})

@manager_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã tạo học phần.')
        return redirect('academics:courses')
    return render(request, 'academics/form.html', {'form': form, 'title': 'Thêm học phần'})

@manager_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã cập nhật học phần.')
        return redirect('academics:courses')
    return render(request, 'academics/form.html', {'form': form, 'title': 'Sửa học phần'})

@staff_required
def section_list(request):
    sections = CourseSection.objects.select_related('course', 'teacher_user')
    if request.user.role == 'LECTURER' and not request.user.is_superuser:
        sections = sections.filter(teacher_user=request.user)
    return render(request, 'academics/section_list.html', {'sections': sections})

@manager_required
def section_create(request):
    form = CourseSectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã tạo lớp học phần.')
        return redirect('academics:sections')
    return render(request, 'academics/form.html', {'form': form, 'title': 'Mở lớp học phần'})

@manager_required
def section_update(request, pk):
    section = get_object_or_404(CourseSection, pk=pk)
    form = CourseSectionForm(request.POST or None, instance=section)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã cập nhật lớp học phần.')
        return redirect('academics:sections')
    return render(request, 'academics/form.html', {'form': form, 'title': 'Sửa lớp học phần'})

@manager_required
def section_close(request, pk):
    section = get_object_or_404(CourseSection, pk=pk)
    if request.method == 'POST':
        section.status = CourseSection.Status.CLOSED
        section.save(update_fields=['status'])
        messages.success(request, 'Đã đóng lớp học phần; dữ liệu đăng ký cũ được giữ nguyên.')
    return redirect('academics:sections')
